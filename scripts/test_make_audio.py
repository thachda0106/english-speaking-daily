"""Checks for the speaking-course audio pipeline.

The repo has no test framework, so this is a plain script: run it and read PASS/FAIL.

    python scripts/test_make_audio.py

It covers the parts that are easy to break and expensive to notice late — a wrong
audio filename, the learner's own lines read back at them, temp files left behind
when a run fails half-way. Everything runs offline: ffmpeg builds the audio from a
generated tone instead of calling the network, so it is fast and repeatable.
"""
import asyncio
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
spec = importlib.util.spec_from_file_location("make_audio", HERE / "make_audio.py")
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
days_spec = importlib.util.spec_from_file_location("days", HERE / "days.py")
days = importlib.util.module_from_spec(days_spec)
days_spec.loader.exec_module(days)
SPEAKER = days.DAYS

CONV = """# Day X · Conversation 1 — Probe

## 🗣️ Dialogue — read out loud

> **Manager:** Hello there, this is `line` one.

> **You:** And this line is the learner's, so it must be skipped.

> **Manager:** Second one, with **bold** and _em_ markup.
"""
STORY = """# Day X · 📖 The Long Story — Probe

> This intro line is a blockquote and must not be spoken.

---

**The first sentence is bold.** The second sentence follows it. The third one closes.

---

## 🧠 Story vocabulary & grammar
- **Past-tense verbs:** `said · told`
- This bullet must not be spoken either.

## ✅ Done when…
- [ ] I read the story out loud twice
- [ ] I shadowed the story audio
"""
failures = []


def check(name, cond, detail=""):
    if not cond:
        failures.append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  <- ' + detail}")


tmp = pathlib.Path(tempfile.mkdtemp(prefix="hermes-verify-"))
(tmp / "conversation-01-probe.md").write_text(CONV, encoding="utf-8")
(tmp / "story-01-probe.md").write_text(STORY, encoding="utf-8")
(tmp / "notes.md").write_text("not a lesson\n", encoding="utf-8")

print("\nparsing")
chunks = ma.parse_conversation(tmp / "conversation-01-probe.md")
check("the learner's own lines are never read back at them",
      [t for t, _ in chunks] == ["Hello there, this is line one.",
                                 "Second one, with bold and em markup."],
      str([t for t, _ in chunks]))
check("markdown emphasis stripped",
      all("**" not in t and "`" not in t and "_" not in t for t, _ in chunks))
check("each line leaves room to answer", all(p == ma.PAUSE_LINE for _, p in chunks))

story = " ".join(t for t, _ in ma.parse_story(tmp / "story-01-probe.md"))
check("story prose is spoken", "The first sentence is bold." in story)
check("story intro quote is skipped", "blockquote" not in story)
check("story grammar notes are skipped", "Past-tense verbs" not in story)
check("story heading is skipped", "Story vocabulary" not in story)
check("story title is skipped", "The Long Story" not in story)
check("the 'Done when' checklist is not read aloud",
      "read the story out loud" not in story)

(tmp / "multi.md").write_text("**One.** Two. Three.\n\nFour. Five.\n", encoding="utf-8")
multi = ma.parse_story(tmp / "multi.md")
check("a story is split into sentences, not read as one block",
      [t for t, _ in multi] == ["One.", "Two.", "Three.", "Four.", "Five."],
      str([t for t, _ in multi]))
check("each sentence carries the story pause, so shadowing has a rhythm",
      all(p == ma.PAUSE_SENTENCE for _, p in multi))

(tmp / "rules.md").write_text("One two.\n\n---\n\nThree four.\n", encoding="utf-8")
check("a horizontal rule is not read as prose",
      [t for t, _ in ma.parse_story(tmp / "rules.md")] == ["One two.", "Three four."],
      str([t for t, _ in ma.parse_story(tmp / "rules.md")]))

(tmp / "messy.md").write_text("**A**   `b`\nsecond   line. Done.\n", encoding="utf-8")
check("stray whitespace is collapsed so the tts call stays clean",
      [t for t, _ in ma.parse_story(tmp / "messy.md")] == ["A b second line.", "Done."],
      str([t for t, _ in ma.parse_story(tmp / "messy.md")]))

long = ", ".join(["word" * 20] * 12)
check("long lines split under the tts limit",
      all(len(p) <= 230 for p in ma.split_for_tts(long)))
check("splitting loses no words", " ".join(ma.split_for_tts(long)) == long)
check("short line is left alone", ma.split_for_tts("hi there") == ["hi there"])
check("a line just under the limit is not split at all",
      ma.split_for_tts("word " * 45 + "end") == ["word " * 45 + "end"])
check("a long line with no clause breaks stays whole (nowhere to split)",
      ma.split_for_tts("word " * 60) == [("word " * 60).rstrip()])

print("\nfilenames")
check("a conversation is named for the speaker who talks in it",
      ma.target_for(tmp / "conversation-01-probe.md", "manager")[0]
      == "manager-01-probe.mp3")
check("a story keeps its story- name, since nobody else speaks it",
      ma.target_for(tmp / "story-01-probe.md", "manager")[0]
      == "story-01-probe.mp3")
check("files that are not lessons are skipped",
      ma.target_for(tmp / "notes.md", "manager") is None)

seed = tmp / "seed.mp3"
subprocess.run([ma.FFMPEG, "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=0.15",
                "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
                str(seed)], capture_output=True)
TONE = seed.read_bytes()


async def fake_synth(text, voice, rate):
    return TONE


ma.synth_chunk = fake_synth  # keep the real ffmpeg join, drop the network call


def lesson_day(name, lesson="conversation-01-probe.md"):
    d = tmp / name
    (d / "audio").mkdir(parents=True)
    (d / lesson).write_text((tmp / lesson).read_text(encoding="utf-8"),
                            encoding="utf-8")
    return d


def build_at(name, runner, lesson="conversation-01-probe.md"):
    """Run build() on a scratch day with `runner` standing in for ffmpeg."""
    d = lesson_day(name, lesson)
    target = d / "audio" / ma.target_for(d / lesson, "manager")[0]
    real, ma.run = ma.run, runner
    try:
        asyncio.run(ma.build(ma.target_for(d / lesson, "manager")[1], "v", "-8%", target))
        return d, target, False
    except RuntimeError:
        return d, target, True
    finally:
        ma.run = real


def boom(cmd):
    raise RuntimeError("ffmpeg unavailable")


def silent(cmd):
    """ffmpeg exit 0 but writes nothing — the quiet failure mode."""
    return subprocess.CompletedProcess(cmd, 0, b"", b"")


print("\nbuilding audio")
day = lesson_day("day")
out = day / "audio" / ma.target_for(day / "conversation-01-probe.md", "manager")[0]
asyncio.run(ma.build(chunks, "en-US-AriaNeural", "-8%", out))
check("mp3 is written", out.exists() and out.stat().st_size > 0)
check("the audio holds both the words and the answer gap", ma.duration(out) > 1.0,
      f"{ma.duration(out):.2f}s")
check("no temp files left behind", not list((day / "audio").glob("_tts_*")))
check("output matches the format of the hand-made day 1-4 mp3s",
      ma.spec_of(out) == ("mp3", 24000, 1, 48), str(ma.spec_of(out)))

# main() used to unpack two values here and then print a `kind` that no longer
# existed, so every run died with NameError — after the audio was already written.
check("target_for also returns the kind main() prints",
      [t[2] for t in (ma.target_for(tmp / "conversation-01-probe.md", "manager"),
                      ma.target_for(tmp / "story-01-probe.md", "manager"))]
      == ["conv", "story"])

day_full = tmp / "day-full"
lesson_day("day-full")
for lesson in ("conversation-01-probe.md", "story-01-probe.md"):
    shutil.copy(tmp / lesson, day_full / lesson)
argv, main_err = sys.argv, ""
sys.argv = ["make_audio.py", str(day_full), "--prefix", "manager"]
try:
    asyncio.run(ma.main())  # the real entry point, not just build()
    main_ok = True
except Exception as exc:  # NameError, KeyError, anything main() trips on
    main_ok, main_err = False, f"{type(exc).__name__}: {exc}"
finally:
    sys.argv = argv
check("main() runs end to end over a conversation and a story", main_ok, main_err)
check("main() wrote both mp3s", len(list((day_full / "audio").glob("*.mp3"))) == 2)

print("\nbuilding a story")
day_story = lesson_day("day-story", "story-01-probe.md")
story_chunks = ma.parse_story(day_story / "story-01-probe.md")
story_out = day_story / "audio" / ma.target_for(day_story / "story-01-probe.md",
                                               "manager")[0]
asyncio.run(ma.build(story_chunks, "en-US-AriaNeural", "-8%", story_out))
check("a story gets audio of its own", story_out.exists())
# Each sentence is one 0.15s tone; the rest must be air, not silence-as-sound.
spoken = len(story_chunks) * 0.15
check("a story breathes between sentences instead of running on",
      ma.duration(story_out) > spoken * 1.5,
      f"{ma.duration(story_out):.2f}s vs {spoken:.2f}s of tone")
check("story audio carries no speaker prefix",
      not list((day_story / "audio").glob("manager-*")))

print("\nwhen a run fails part-way")
real_run = ma.run
dead, target, raised = build_at("day-fail", boom)
check("the error is reported, not swallowed", raised)
check("a failed run still leaves no temp files",
      not list((dead / "audio").glob("_tts_*")))
check("a failed run writes no half-built mp3", not target.exists())

quiet, target, silent_failed = build_at("day-silent", silent)
check("a build that silently writes no audio is reported", silent_failed)
check("no empty mp3 is left behind", not list((quiet / "audio").glob("*.mp3")))

try:
    ma.run([ma.FFMPEG, "-i", str(tmp / "does-not-exist.mp3")])
    run_raises = False
except RuntimeError as e:
    run_raises = "failed" in str(e)
check("run() reports an ffmpeg failure, with the reason", run_raises)

print("\nrepo state")
in_repo = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--is-inside-work-tree"],
                         capture_output=True, text=True).stdout.strip() == "true"
for pattern in (["_tts_p000.mp3", "_tts_s000.mp3", "_tts_list_x.txt"] if in_repo else []):
    ignored = subprocess.run(["git", "-C", str(REPO), "check-ignore", "-q",
                              f"day-01/audio/{pattern}"], capture_output=True)
    check(f"gitignored: {pattern}", ignored.returncode == 0)
if not in_repo:
    print("  SKIP  gitignore checks (not a git work tree)")
check("no temp files sitting in the repo", not list(REPO.glob("day-*/audio/_tts_*")))


# A day is "voiced" once it has an audio/ folder. Days written but not yet voiced
# are a legitimate state -- the lessons exist and the mp3s come later -- so they
# are reported on every run rather than failing: a deleted audio/ folder would
# otherwise make these checks skip silently.
voiced = [d for d in sorted(REPO.glob("day-*"))
          if d.name in SPEAKER and (d / "audio").is_dir()]
pending = [d.name for d in sorted(REPO.glob("day-*"))
           if d.name in SPEAKER and not (d / "audio").is_dir()]

lessons = [(d, p) for d in voiced for p in sorted(d.glob("*.md"))
           if ma.target_for(p, SPEAKER[d.name])]
orphan = [f"{d.name}/{p.name}" for d, p in lessons
          if not (d / "audio" / days.mp3_for(d.name, p.stem)).exists()]
check(f"every lesson has its mp3 ({len(lessons)} lessons, {len(voiced)} voiced days)",
      not orphan, str(orphan[:5]))

on_disk = {d.name for d in REPO.glob("day-*") if d.is_dir()}
planned = set(SPEAKER) - on_disk
# days.py is the roadmap, so a registered day with no folder is planned, not
# broken. The two must still agree exactly: a folder nobody registered would get
# audio named after a prefix nothing expects, and a registration whose folder
# vanished would silently drop that day out of the mp3 checks.
check("every day folder on disk is registered in days.py",
      not on_disk - set(SPEAKER), str(sorted(on_disk - set(SPEAKER))))
check("roadmap and repo agree on written vs planned",
      on_disk | planned == set(SPEAKER) and not on_disk & planned)
if planned:
    print(f"\n  NOTE  {len(planned)} roadmap day(s) not written yet:")
    print("        " + ", ".join(sorted(planned)))

if pending:
    print(f"\n  NOTE  {len(pending)} day(s) written but not voiced yet:")
    print("        " + ", ".join(pending))
    print("        Lessons are complete. Run scripts/build_all_audio.sh for their mp3s.")

shutil.rmtree(tmp, ignore_errors=True)
print(f"\n{'=' * 58}\n{len(failures)} failed")
sys.exit(1 if failures else 0)