"""Format audit for the lesson files.

    python scripts/audit_lessons.py [day-folder ...]

Not a pass/fail test -- it reports. Each day has 5 conversations and 1 story; a
conversation carries Situation / Dialogue / vocabulary / After you speak / Done
when, and a story carries prose / vocabulary / exercise / Done when.

Headings are matched on their leading emoji rather than on the whole line,
because several days extend them ("## Dialogue -- read out loud...") and an
exact-match audit reports those as missing sections when they are present.

Banned spoken words are checked only against dialogue lines ("> **Name:**"),
never against the whole file: they belong in prose about the lesson, just not in
something a learner would have to say out loud.
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


def spoken_lines(text):
    return "\n".join(l for l in text.splitlines() if l.strip().startswith("> **"))


def banned_in(text):
    """Banned words, matched on word boundaries.

    A substring match reports "slo" inside "slowly", which is how a fluency
    lesson about speaking slowly got flagged for an SLO.
    """
    found = []
    for word in BANNED_SPOKEN:
        if re.search(rf"\b{re.escape(word)}\b", text, re.I):
            found.append(word)
    return found


def prose_words(text, story):
    """Word count of the lesson's own prose, ignoring markdown furniture."""
    body = text
    for line in body.splitlines():
        if line.strip().startswith(">"):
            body = body.replace(line, "")
    body = re.sub(r"`[^`]*`", "", body)
    return len(re.findall(r"[A-Za-z][A-Za-z'-]+", body))


def audit(day):
    d = REPO / day
    rows = []
    for f in sorted(d.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        story = f.name.startswith("story-")
        needed = STORY if story else CONVERSATION
        heads = re.findall(r"^##+ (.+)$", text, re.M)
        missing = [s for s in needed if not any(h.startswith(s) for h in heads)]
        banned = banned_in(spoken_lines(text))
        turns = len(re.findall(r"^> \*\*[^:*]+:\*\*", text, re.M))
        truncated = text.rstrip().endswith(("…", "...")) and len(text) < 900
        problems = []
        if missing:
            problems.append(f"missing headings {missing}")
        if banned:
            problems.append(f"banned in spoken {banned}")
        if story and turns:
            problems.append(f"story has {turns} dialogue turns")
        # 6 is the floor the shipped days already meet (day-09 is all sixes),
        # so anything lower is a genuinely thin conversation, not a style choice.
        if not story and turns < 6:
            problems.append(f"only {turns} dialogue turns")
        rows.append((f.name, story, prose_words(text, story), turns, problems))
    return rows


def main(argv):
    days = argv[1:] or sorted(
        p.name for p in REPO.glob("day-*")
        if p.is_dir() and p.name[4:6].isdigit() and int(p.name[4:6]) >= 11)
    total_bad = 0
    for day in days:
        if not (REPO / day).is_dir():
            print(f"{day}: NOT ON DISK")
            continue
        rows = audit(day)
        bad = [r for r in rows if r[4]]
        total_bad += len(bad)
        words = sum(r[2] for r in rows if r[1])
        conv = sum(1 for r in rows if not r[1])
        print(f"\n{day}  {conv} conversations + {len(rows)-conv} story"
              f"  ({words} words of story prose)")
        for name, story, w, turns, problems in rows:
            tag = "story" if story else f"{turns:>2} turns"
            status = "FAIL" if problems else "PASS"
            print(f"  {status}  {name:<50}{w:>5}w  {tag}")
            for p in problems:
                print(f"        -> {p}")
    print(f"\n{'=' * 66}\n{total_bad} problem(s)")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))