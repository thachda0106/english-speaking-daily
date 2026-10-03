"""Checks for scripts/days.py and the day registry it drives.

    python scripts/test_days.py

scripts/test_make_audio.py and scripts/build_all_audio.sh both depend on the day
registry, and all three fail the same silent way: a day missing from the registry
means its audio gets named after a prefix nobody checks for, and nothing reports
it. This keeps the registry honest on its own terms.

Runs offline. No edge-tts, no network.
"""
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
spec = importlib.util.spec_from_file_location("days", HERE / "days.py")
days = importlib.util.module_from_spec(spec)
spec.loader.exec_module(days)

failures, passes = [], 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
    else:
        failures.append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  <- ' + detail}")


print("\nregistry shape")
check("every key is a day-NN-slug folder",
      all(re.fullmatch(r"day-\d\d-[a-z-]+", d) for d in days.DAYS),
      str([d for d in days.DAYS if not re.fullmatch(r"day-\d\d-[a-z-]+", d)]))
numbers = sorted(d[4:6] for d in days.DAYS)
check("day numbers are contiguous 01..NN",
      numbers == [f"{n:02d}" for n in range(1, len(numbers) + 1)], str(numbers))
check("every speaker is a bare lowercase prefix",
      all(re.fullmatch(r"[a-z]+", s) for s in days.DAYS.values()),
      str([(d, s) for d, s in days.DAYS.items() if not re.fullmatch(r"[a-z]+", s)]))

print("\nmp3_for -- the contract between the generator and the tests")
check("conversation -> <speaker>-NN-slug.mp3",
      days.mp3_for("day-11-coffee-shop", "conversation-01-ordering-a-coffee")
      == "friend-01-ordering-a-coffee.mp3",
      days.mp3_for("day-11-coffee-shop", "conversation-01-ordering-a-coffee"))
check("story keeps its name and gets no speaker prefix",
      days.mp3_for("day-27-workplace-small-talk", "story-01-the-long-story")
      == "story-01-the-long-story.mp3",
      days.mp3_for("day-27-workplace-small-talk", "story-01-the-long-story"))
check("a two-digit lesson number is not truncated",
      days.mp3_for("day-10-technical-interview", "conversation-05-your-questions")
      == "interviewer-05-your-questions.mp3",
      days.mp3_for("day-10-technical-interview", "conversation-05-your-questions"))
check("legacy day-02 slug override honoured",
      days.mp3_for("day-02-phone-screen", "conversation-04-salary-and-working-style")
      == "recruiter-04-salary.mp3",
      days.mp3_for("day-02-phone-screen", "conversation-04-salary-and-working-style"))
check("legacy day-04 slug override honoured",
      days.mp3_for("day-04-daily-standup", "conversation-01-the-stand-up-format")
      == "standup-01-the-format.mp3",
      days.mp3_for("day-04-daily-standup", "conversation-01-the-stand-up-format"))
check("an override applies to one lesson only, not the whole day",
      days.mp3_for("day-02-phone-screen", "conversation-05-next-steps")
      == "recruiter-05-next-steps.mp3",
      days.mp3_for("day-02-phone-screen", "conversation-05-next-steps"))
check("every override key names a real day and lesson number",
      all(d in days.DAYS and re.fullmatch(r"\d\d", n) for d, n in days.LEGACY_SLUGS),
      str(days.LEGACY_SLUGS))

print("\nconsumers do not duplicate the registry")
test_src = (HERE / "test_make_audio.py").read_text(encoding="utf-8")
check("test_make_audio.py imports days.py",
      'spec_from_file_location("days"' in test_src and "SPEAKER = days.DAYS" in test_src)
duplicated = [d for d in days.DAYS if f'"{d}":' in test_src]
check("no day->speaker pair is hardcoded in the test", not duplicated, str(duplicated))
shell = (HERE / "build_all_audio.sh").read_text(encoding="utf-8")
check("build_all_audio.sh reads days.py", "days.py" in shell)
check("build_all_audio.sh hardcodes no day list",
      not re.search(r"^run_day day-\d\d", shell, re.M))
check("build_all_audio.sh still fails loudly",
      "failed+=(" in shell and "exit 1" in shell and "FINISHED WITH ERRORS" in shell)

print("\nrepo agreement")
folders = sorted(d.name for d in REPO.glob("day-*") if d.is_dir())
unregistered = [d for d in folders if d not in days.DAYS]
check("every day folder on disk is registered", not unregistered, str(unregistered))
missing = [d for d in days.DAYS if not (REPO / d).is_dir()]
if missing:
    print(f"  NOTE  {len(missing)} registered day(s) not written yet:")
    print("        " + ", ".join(missing))
else:
    check("every registered day exists on disk", True)

print(f"\n{'=' * 58}\n{passes} passed, {len(failures)} failed")
if failures:
    print("FAILED:", *failures, sep="\n  - ")
sys.exit(1 if failures else 0)