"""Format audit for the lesson files.

    python scripts/audit_lessons.py [day-folder ...]

It reports rather than asserts. Each day is 5 conversations and 1 story: a
conversation carries Situation / Dialogue / vocabulary / After you speak / Done
when, and a story carries prose / vocabulary / exercise / Done when.

Two deliberate loosenesses, both earned:

  * headings match on their leading emoji, not the whole line, because several
    days extend them ("## Dialogue -- read out loud...") and an exact match
    calls those missing sections when they are there
  * banned words match on word boundaries, because a substring match reports
    "slo" inside "slowly" -- which is how the speaking-slowly lesson got flagged
    for an SLO

Banned words are checked only against dialogue lines ("> **Name:**"): they belong
in prose about the lesson, just not in something a learner has to say out loud.

scripts/test_audit_lessons.py covers this module.
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

CONVERSATION = ["🎬", "🗣️", "🧠", "✅ After you speak", "✅ Done when"]
STORY = ["🧠", "✏️", "✅ Done when"]

BANNED_SPOKEN = [
    "root cause", "mitigation", "regression", "postmortem", "counteroffer",
    "equity", "vesting", "slo", "sla", "rollback", "blast radius",
]

MIN_TURNS = 6  # day-09 is all sixes, so lower than this is thin, not a style


def spoken_lines(text):
    return "\n".join(l for l in text.splitlines() if l.strip().startswith("> **"))


def banned_in(text):
    found = [w for w in BANNED_SPOKEN
             if re.search(rf"\b{re.escape(w)}\b", text, re.I)]
    return found


def turns(text):
    return len(re.findall(r"^> \*\*[^:*]+:\*\*", text, re.M))


def prose_words(text):
    """Words of the lesson's own prose, ignoring dialogue and inline code.

    Two details, both paid for in bugs:

    * the code span is [^`]+ rather than `[^`]*` -- a regex is itself common
      lesson content, and "`findall`/`rfind` are list methods" would otherwise be
      eaten whole, taking the words either side of it with it
    * a word is \\w with a trailing +, not [A-Za-z][A-Za-z'-]+ -- the latter
      needs two characters, so the one-letter words that survive inline-code
      removal ("a `b` c" -> "a  c") counted as nothing
    """
    body = "\n".join(l for l in text.splitlines() if not l.strip().startswith(">"))
    return len(re.findall(r"\b[\w'-]+\b", re.sub(r"`[^`]+`", "", body)))


def problems_for(text, story):
    """Every way this lesson is wrong. Empty list means it is fine."""
    needed = STORY if story else CONVERSATION
    heads = re.findall(r"^##+ (.+)$", text, re.M)
    n = turns(text)
    out = []
    if missing := [s for s in needed if not any(h.startswith(s) for h in heads)]:
        out.append(f"missing headings {missing}")
    if banned := banned_in(spoken_lines(text)):
        out.append(f"banned in spoken {banned}")
    if story and n:
        out.append(f"story has {n} dialogue turns")
    elif not story and n < MIN_TURNS:
        out.append(f"only {n} dialogue turns")
    return out


def audit(day):
    """(filename, is_story, prose_words, turns, problems) per lesson file."""
    rows = []
    for f in sorted((REPO / day).glob("*.md")):
        text = f.read_text(encoding="utf-8")
        story = f.name.startswith("story-")
        rows.append((f.name, story, prose_words(text), turns(text),
                     problems_for(text, story)))
    return rows


def main(argv):
    days = argv[1:] or sorted(
        p.name for p in REPO.glob("day-*")
        if p.is_dir() and p.name[4:6].isdigit() and int(p.name[4:6]) >= 11)
    bad = 0
    for day in days:
        if not (REPO / day).is_dir():
            print(f"{day}: NOT ON DISK")
            continue
        rows = audit(day)
        bad += sum(1 for r in rows if r[4])
        conv = sum(1 for r in rows if not r[1])
        print(f"\n{day}  {conv} conversations + {len(rows) - conv} story"
              f"  ({sum(r[2] for r in rows if r[1])} words of story prose)")
        for name, story, words, n, probs in rows:
            print(f"  {'FAIL' if probs else 'PASS'}  {name:<50}{words:>5}w  "
                  f"{'story' if story else f'{n:>2} turns'}")
            for p in probs:
                print(f"        -> {p}")
    print(f"\n{'=' * 66}\n{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))