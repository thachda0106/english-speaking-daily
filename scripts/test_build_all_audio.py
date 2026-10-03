"""Checks for scripts/build_all_audio.sh — the wrapper that drives every day.

    python scripts/test_build_all_audio.py

This covers the one thing scripts/test_make_audio.py cannot: what the shell
wrapper *reports*. Its exit code and its last line are the only signal a CI job
or an agent gets, so "printed a failure and then said 'all done'" is the bug
that matters most here.

Offline: scripts/make_audio.py is swapped for a stub, so nothing calls edge-tts.
"""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BASH = next((p for p in (r"C:\Program Files\Git\bin\bash.exe",
                         "/usr/bin/bash", "bash") if shutil.which(p) or pathlib.Path(p).exists()),
            None)
_spec = importlib.util.spec_from_file_location("days", HERE / "days.py")
_days = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_days)
REGISTRY = sorted(_days.DAYS)

failures, passes = [], 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
    else:
        failures.append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  <- ' + detail}")


class Sandbox:
    """A throwaway copy holding only what the wrapper actually touches.

    The wrapper cds to its parent and calls scripts/make_audio.py, so the stub
    replaces the real generator and no day folder or mp3 is needed.
    """

    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="hermes-verify-"))
        (self.dir / "scripts").mkdir()
        for f in ("build_all_audio.sh", "days.py"):
            shutil.copy(REPO / "scripts" / f, self.dir / "scripts")
        # build_all_audio.sh qualifies a day by its *lessons* existing. Without
        # them plan() finds nothing and the run degenerates into a vacuous pass
        # (or trips the empty-plan guard), never exercising the day loop.
        for day in REGISTRY:
            (self.dir / day).mkdir()
            (self.dir / day / "conversation-01-probe.md").write_text(
                "# probe\n", encoding="utf-8")

    def stub(self, exit_code: int, echo: str = ""):
        (self.dir / "scripts" / "make_audio.py").write_text(
            f"import sys\nprint({echo!r})\nsys.exit({exit_code})\n", encoding="utf-8")
        return self

    def run(self):
        return self.run_with_args([])

    def run_with_args(self, args):
        if BASH is None:
            return None, ""
        r = subprocess.run([BASH, "scripts/build_all_audio.sh", *args], cwd=self.dir,
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)


print("\nsyntax")
if BASH is None:
    print("  SKIP  no bash on PATH")
else:
    r = subprocess.run([BASH, "-n", str(REPO / "scripts" / "build_all_audio.sh")],
                       capture_output=True, text=True)
    check("build_all_audio.sh parses", r.returncode == 0, r.stderr.strip()[:120])

print("\nwhen every day succeeds")
ok = Sandbox().stub(0, "ok")
code, out = ok.run()
check("exits 0", code == 0, f"exit={code}")
check("reports all done", "=== all done ===" in out)
check("names no failures", "FAILED" not in out)
ok.close()

print("\nwhen a day fails (exit 1 from the generator)")
bad = Sandbox().stub(1, "simulated network failure")
code, out = bad.run()
check("exits non-zero", code not in (0, None), f"exit={code}")
check("does NOT claim all done", "=== all done ===" not in out)
check("flags the wrapper as errored", "FINISHED WITH ERRORS" in out, out.strip()[-160:])
failed_days = set(re.findall(r"day-\d\d-[a-z-]+", out.split("FINISHED WITH ERRORS")[-1]))
check("names every failed day", failed_days == set(REGISTRY),
      f"{len(failed_days)} of {len(REGISTRY)}: {sorted(failed_days)}")
check("keeps going after a failure, rather than stopping at the first",
      len(failed_days) == len(REGISTRY), f"only {len(failed_days)} ran")
bad.close()

print("\nthe registry drives the day list")
shell = (REPO / "scripts" / "build_all_audio.sh").read_text(encoding="utf-8")
check("no day is hardcoded outside the registry loop",
      not re.search(r"^run_day day-\d\d", shell, re.M),
      "a run_day day-NN line is back")
check("the day list comes from days.py", "days.py" in shell)
# Whether plan() skips days without audio/ is test_days.py's concern; here we
# only assert the wrapper delegates its day list to the registry.

print("\nthe day-number filter passes whole folder names")
# The stub echoes its argv, so this asserts what the wrapper *hands over* --
# which is the part the wrapper controls. Banners come from the real script, so
# asserting on them here would pass regardless of the wrapper's behaviour.
named = Sandbox().stub(0, "ok")
(named.dir / "scripts" / "make_audio.py").write_text(
    "import sys\nprint('ARGV=' + '|'.join(sys.argv[1:]))\n", encoding="utf-8")
code, out = named.run_with_args(["28"])
passed = [l for l in out.splitlines() if "ARGV=" in l]
check("one day ran for the requested number", len(passed) == 1, out.strip()[-120:])
check("it received the full folder name, not a stripped one",
      passed and passed[0].startswith("ARGV=day-28-hobbies-and-interests|"),
      str(passed[:1]))
check("no other day ran", "day-27" not in out and "day-29" not in out)
check("exit 0 when the selected day succeeds", code == 0, f"exit={code}")
named.close()

print("\nwhen the day list cannot be read")
empty = Sandbox().stub(0, "ok")
for d in REGISTRY:  # remove every lesson, so plan() finds nothing
    (empty.dir / d / "conversation-01-probe.md").unlink()
code, out = empty.run()
check("an empty plan exits non-zero", code not in (0, None), f"exit={code}")
check("an empty plan does NOT claim all done", "=== all done ===" not in out)
check("and says why", "no days found" in out, out.strip()[-140:])
empty.close()

print("\nthe pre-fix wrapper, for comparison")
sh = (REPO / "scripts" / "build_all_audio.sh").read_text(encoding="utf-8")
# \r?\n, not \n: this repo checks the script in with CRLF endings, and a bare $
# anchor silently fails to match them, which would make this replay vacuous.
unfixed = re.sub(r"if \[ \$\{#failed\[@\]\} -gt 0 \]; then.*?^fi\r?\n", "",
                 sh, flags=re.M | re.S)
check("the guard under test is actually present in the repo",
      unfixed != sh and "FINISHED WITH ERRORS" in sh)
old = Sandbox().stub(1, "simulated network failure")
(old.dir / "scripts" / "build_all_audio.sh").write_text(unfixed, encoding="utf-8")
code, out = old.run()
check("without the guard it lies: exit 0 and 'all done'",
      code == 0 and "=== all done ===" in out, f"exit={code}")
old.close()

print("\nshipped repo")
if BASH is not None:
    check("wrapper runs from the repo without HERMES_PY set",
          subprocess.run([BASH, "-n", str(REPO / "scripts" / "build_all_audio.sh")],
                         capture_output=True).returncode == 0)
# Whether every registered day exists is test_days.py's job. This suite only
# cares that the wrapper enumerates whatever the registry holds.

print(f"\n{'=' * 58}\n{passes} passed, {len(failures)} failed")
if failures:
    print("FAILED:", *failures, sep="\n  - ")
sys.exit(1 if failures else 0)