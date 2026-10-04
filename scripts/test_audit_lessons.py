"""Checks for scripts/audit_lessons.py.

    python scripts/test_audit_lessons.py

The audit is a reporter, and a reporter that always says PASS is worse than no
reporter -- it looks like evidence. So most of this suite feeds it deliberately
broken lessons and asserts it objects, rather than just running it against the
repo and reading the output.

Offline and instant: no network, no TTS, no repo writes.
"""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
_spec = importlib.util.spec_from_file_location("audit", HERE / "audit_lessons.py")
al = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(al)
PY = sys.executable

failures, passes = [], 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
    else:
        failures.append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  <- ' + detail}")


def dialogue(n, extra=None):
    out = [f"> **{'You' if i % 2 else 'Friend'}:** Line {i + 1}.\n" for i in range(n)]
    if extra:
        out.append(f"> **Friend:** {extra}\n")
    return "".join(out)


def conv(turns=8, vocab="- **thing** — a note", extra=None):
    return (f"# Day · Conversation 1 — Title\n\n## 🎬 Situation\nSome situation.\n\n"
            f"## 🗣️ Dialogue\n{dialogue(turns, extra)}\n"
            f"## 🧠 Your active vocabulary\n{vocab}\n\n"
            f"## ✅ After you speak\n**Formula:** *do it like this*\n\n"
            f"## ✅ Done when…\n- …it works\n")


STORY = ("# Day · 📖 The Long Story — Title\n\n> A note.\n\n%s\n\n"
         "## ✅ After you speak\n**Formula:** *thing*\n\n"
         "## 🧠 Your active vocabulary\n- **word**\n\n"
         "## ✏️ Speak for 60 seconds\n*Say something.*\n\n"
         "## ✅ Done when…\n- …it works\n")
PROSE = ("The shop was quiet and I said something. " * 47).strip()


def day(**over):
    files = {f"conversation-0{i}-x.md": conv() for i in range(1, 6)}
    files["story-01-the-long-story.md"] = STORY % PROSE
    return files.update(over) or files


def sandbox(files):
    """A repo-shaped tree so main() can be run end to end."""
    box = pathlib.Path(tempfile.mkdtemp(prefix="audit-test-"))
    (box / "scripts").mkdir()
    shutil.copy(HERE / "audit_lessons.py", box / "scripts" / "audit_lessons.py")
    (box / "day-99-test").mkdir()
    for name, text in files.items():
        (box / "day-99-test" / name).write_text(text, encoding="utf-8")
    return box


def run(box, *days):
    r = subprocess.run([PY, str(box / "scripts" / "audit_lessons.py"), *days],
                       cwd=str(box), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def rejects(label, text, key="conversation-01-x.md"):
    box = sandbox(day(**{key: text}))
    code, out = run(box, "day-99-test")
    shutil.rmtree(box.parent, ignore_errors=True)
    ok = code != 0 and "0 problem(s)" not in out
    check(f"flags {label}", ok, out.strip().splitlines()[-1] if out.strip() else "")


print("\nunit: problems_for, no files needed")
check("a well-formed conversation has no problems", al.problems_for(conv(), False) == [])
check("a well-formed story has no problems", al.problems_for(STORY % PROSE, True) == [])
check("a missing heading is reported",
      "missing headings" in " ".join(al.problems_for(
          conv().replace("## 🧠 Your active vocabulary", "## Notes"), False)))
check("a thin conversation is reported",
      any("dialogue turns" in p for p in al.problems_for(conv(turns=4), False)))
check("exactly MIN_TURNS is fine", al.problems_for(conv(turns=al.MIN_TURNS), False) == [])
check("a banned word in speech is reported",
      any("banned" in p for p in al.problems_for(
          conv(extra="the root cause was a bad deploy"), False)))
check("a story carrying dialogue is reported",
      any("dialogue turns" in p for p in al.problems_for(
          (STORY % PROSE).replace("## ✏️ Speak", dialogue(8) + "\n## ✏️ Speak"), True)))

print("\nunit: the two deliberate loosenesses")
check("a lengthened heading still satisfies its section",
      al.problems_for(conv().replace("## 🗣️ Dialogue",
                                     "## 🗣️ Dialogue — read out loud, then play"), False) == [])
check("'slowly' is not an 'slo'", al.banned_in("Speak slowly, take a slow turn, slot it in.") == [])
check("a real SLA is still caught", al.banned_in("We breached the SLA again.") == ["sla"])
check("'root cause' is caught, not 'cause'",
      al.banned_in("the root cause was a deploy") == ["root cause"])
check("banned words in a vocabulary box are fine",
      al.problems_for(conv(vocab="- **rollback** — the postmortem you skip"), False) == [])

print("\nunit: stray vocab")
CONVS = ["a day where you say: there are loads, and he said no worries\n"
         "> **Friend:** That was the hard part, wasn't it?\n"]
check("a phrase taught in a conversation passes",
      al.stray_vocab(CONVS, "## 🧠 Your active vocabulary\n- **no worries** · **there are loads**\n") == [])
check("a phrase taught nowhere is reported",
      al.stray_vocab(CONVS, "## 🧠 Your active vocabulary\n- **can you take the lid off**\n")
      == ["can you take the lid off"])
check("a template with ___ is skipped",
      al.stray_vocab(CONVS, "## 🧠 Your active vocabulary\n- **a bit X, but the Y is good**\n") == [])
check("the story's bolded opening is not treated as vocab",
      al.stray_vocab(CONVS, "**I can cook exactly one thing.**\n\n"
                            "## 🧠 Your active vocabulary\n- **no worries**\n") == [])
check("a one-word item is not checked",
      al.stray_vocab(CONVS, "## 🧠 Your active vocabulary\n- **no** · **hmm** · **thanks**\n") == [])

print("\nunit: counting")
# 8 dialogue lines and no "extra", so exactly 8 -- headings are not turns.
check("dialogue turns are counted, headings are not",
      al.turns(conv(turns=8)) == 8, str(al.turns(conv(turns=8))))
check("an added line is counted",
      al.turns(conv(turns=8, extra="one more")) == 9)
# "> hidden" goes entirely; "a `b` c" keeps a and c once the code span is dropped.
check("prose excludes dialogue lines and inline code",
      al.prose_words("a `b` c\n> hidden\n") == 2,
      str(al.prose_words("a `b` c\n> hidden\n")))
check("one-letter words count, and a regex in a code span does not eat the line",
      al.prose_words("`findall`/`rfind` are list methods\n") == 3,
      str(al.prose_words("`findall`/`rfind` are list methods\n")))
check("a conversation's own prose is counted",
      0 < al.prose_words(conv()) < 200, str(al.prose_words(conv())))

print("\nend to end: main() over a sandbox repo")
box = sandbox(day())
code, out = run(box, "day-99-test")
check("a correct day exits 0", code == 0 and "0 problem(s)" in out,
      out.strip().splitlines()[-1] if out.strip() else "")
check("it reports the shape", "5 conversations + 1 story" in out)
shutil.rmtree(box.parent, ignore_errors=True)

print("\nend to end: main() objects to real defects")
rejects("a missing section", conv().replace("## 🧠 Your active vocabulary", "## Notes"))
rejects("a conversation that is too thin", conv(turns=4))
rejects("a banned word in a spoken line", conv(extra="the root cause was a bad deploy"))
rejects("a story that is actually a dialogue",
        (STORY % PROSE).replace("## ✏️ Speak", dialogue(8) + "\n## ✏️ Speak"),
        key="story-01-the-long-story.md")

print("\nthe real repo")
NEW = ["day-11-coffee-shop", "day-12-grocery-shopping", "day-13-taking-a-bus"]
LEGACY = ["day-27-workplace-small-talk", "day-28-hobbies-and-interests",
          "day-29-storytelling-past-experiences", "day-30-sounding-natural"]


def audit(day_name):
    return subprocess.run([PY, str(HERE / "audit_lessons.py"), day_name], cwd=str(REPO),
                          capture_output=True, text=True).stdout


check(f"the {len(NEW)} days written most recently audit clean",
      all("FAIL" not in audit(d) for d in NEW), str([d for d in NEW if "FAIL" in audit(d)]))
# Days 27-30 predate the audit and ship cosmetic deviations: three conversations
# run 5 turns and the stories use another heading style. Pinned as a count, so a
# new deviation still shows up instead of passing as "known".
known = sum(audit(d).count("FAIL") for d in LEGACY)
check(f"days 27-30 hold at their {known} known cosmetic deviations", known == 8,
      f"{known}, expected 8")
check("none of them is a banned spoken word",
      all("banned in spoken" not in audit(d) for d in LEGACY))

print(f"\n{'=' * 58}\n{passes} passed, {len(failures)} failed")
if failures:
    print("FAILED:", *failures, sep="\n  - ")
sys.exit(1 if failures else 0)