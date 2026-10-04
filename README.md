# 🗣️ English Speaking Daily

Daily speaking course for Thach — **5 conversations per day**, each one a **long, real dialogue** you **read out loud**.

Replaces "learning lessons" with **speaking practice**: every dialogue is built from vocabulary you already know, so you are *activating* words, not memorizing new ones.

## The daily method (≈ 25 min)

For each of the 5 conversations:

1. **Read silently once** — understand the situation.
2. **Play the speaker MP3** (`audio/<speaker>-XX.mp3`) — the other person speaks with pauses. Answer out loud with your "You:" lines from the conversation file.
3. **Read out loud as both roles** — first the interviewer, then you. Fix your pronunciation as you go.
4. **Record yourself** (phone voice memo) — listen back, pick ONE thing to fix.
5. **Mark it done** in the day's checklist.

> Never practice silently in your head. **The voice is the skill.**

## The long story (from Day 5 on) — do this FIRST

Every day also has **one long story** (`story-01-the-long-story.md` + `.mp3`): the whole day
told as a single narrative in the past tense.

1. **Read it silently once.**
2. **Read it out loud twice.** Stop at every full stop. Feel the past-tense endings.
3. **Shadow the audio** — listen, then repeat each sentence over the top of it.
4. **Retell it in 60 seconds** without looking. This is the real test.

Connected speech is the goal: not single words, but *one long breath of real English*.

## Structure

```
day-01-job-interview/
  conversation-01-greeting.md        → full dialogue + your active vocabulary
  conversation-02-about-yourself.md
  conversation-03-current-project.md
  conversation-04-your-questions.md
  conversation-05-career-plans.md
  audio/
    interviewer-01-greeting.mp3       → interviewer's lines only (you answer)
    interviewer-02-about-yourself.mp3
    interviewer-03-current-project.mp3
    interviewer-04-your-questions.mp3
    interviewer-05-career-plans.mp3
day-02-phone-screen/
  conversation-01-answering-the-call.md
  conversation-02-about-the-position.md
  conversation-03-your-experience.md
  conversation-04-salary-and-working-style.md
  conversation-05-next-steps.md
  audio/
    recruiter-01-answering-the-call.mp3  → recruiter's lines only (you answer)
    recruiter-02-about-the-position.mp3
    recruiter-03-your-experience.mp3
    recruiter-04-salary.mp3
    recruiter-05-next-steps.mp3
day-03-new-team/
  conversation-01-first-day.md
  conversation-02-introducing-yourself.md
  conversation-03-getting-up-to-speed.md
  conversation-04-asking-for-help.md
  conversation-05-small-talk-and-closing.md
  audio/
    team-01-first-day.mp3   → teammate/lead's lines only (you answer)
    team-02-introducing-yourself.mp3
    team-03-getting-up-to-speed.mp3
    team-04-asking-for-help.mp3
    team-05-small-talk-and-closing.mp3
day-04-daily-standup/
  conversation-01-the-stand-up-format.md
  conversation-02-reporting-progress.md
  conversation-03-being-blocked.md
  conversation-04-listening-and-pairing.md
  conversation-05-ending-the-stand-up.md
  audio/
    standup-01-the-format.mp3   → team lead/colleague's lines only (you answer)
    standup-02-reporting-progress.mp3
    standup-03-being-blocked.mp3
    standup-04-listening-and-pairing.mp3
    standup-05-ending-the-stand-up.mp3
day-05-code-review/           prefix: colleague
day-06-explaining-a-bug/      prefix: manager
day-07-salary-discussion/     prefix: recruiter
day-08-negotiating-a-deadline/ prefix: manager
day-09-small-talk-at-lunch/   prefix: colleague
day-10-technical-interview/   prefix: interviewer
  # every day above also has:
  story-01-the-long-story.md + audio/story-01-the-long-story.mp3
```

## Regenerating the audio

All MP3s are generated from the markdown with one script (48 kb/s, 24 kHz, mono):

```bash
python scripts/make_audio.py day-06-explaining-a-bug --prefix manager
python scripts/make_audio.py day-10-technical-interview --prefix interviewer
```

It reads only the **other speaker's** lines from each conversation, adds a 2.6 s pause after
each one so you can answer out loud, and reads the story sentence by sentence. Re-run it any
time you edit a dialogue — never hand-edit an mp3.

## Vocabulary note

Each dialogue only uses words you already know from work and daily life:

`interview · role · team · project · system · backend · API · database · PostgreSQL · query · index · bug · fix · deploy · test · stand-up · code review · manager · requirement · deadline · problem · solution · decision · experience · skill · salary`

New words appear **only** in the 💡 boxes, never inside the dialogue you must speak.

## Roadmap

- [x] Day 1 — The Job Interview
- [x] Day 2 — Phone Screen with a Recruiter
- [x] Day 3 — Introducing Yourself to a New Team
- [x] Day 4 — Daily Stand-up
- [x] Day 5 — Code Review
- [x] Day 6 — Explaining a Bug to a Manager
- [x] Day 7 — Salary Discussion
- [x] Day 8 — Negotiating a Deadline
- [x] Day 9 — Small Talk at Lunch
- [x] Day 10 — The Technical Interview

## Part 1 · Days 1-10 — Workplace English

Built for the job search. Every day is a situation you will actually be in at work.

| Day | Skill it trains | Why it matters for your job search |
| --- | --- | --- |
| 1 | Interview warm-up | The first impression |
| 2 | Phone screen | The call that decides if there is an interview |
| 3 | Joining a new team | What the first 3 months really sound like |
| 4 | Stand-up | Daily proof you can work in English |
| 5 | Code review | Proving you can defend a decision |
| 6 | Explaining a bug | **The question that fails most candidates** |
| 7 | Salary | Asking for more without sounding greedy |
| 8 | Negotiating a deadline | Senior engineers push back; juniors just agree |
| 9 | Small talk | Where you actually build trust at a new company |
| 10 | Technical interview | The whole toolkit, used together |

Day 10, Conversation 5 has **your interview toolkit** — 8 sentences that cover the whole course.
Read it before every interview.

## Part 2 · Days 11-30 — Everyday Conversational English

Days 1-10 taught you to *work* in English. Days 11-30 teach you to *live* in it —
the coffee shop, the bus, the phone call, the rent, the weekend. Nobody is testing
you, so there is nothing to be afraid of and no vocabulary to memorise.

The design is the same: **the dialogue only uses words you already know.** New words
appear only in the 💡 boxes. So each day is not studying — it is activating what is
already in you, out loud, until it stops feeling like English.

| Day | Topic | The sentence it builds |
| --- | --- | --- |
| 11 | Coffee shop | Ordering, and changing your mind |
| 12 | Grocery shopping | Asking for things, comparing two options |
| 13 | Taking a bus | Directions, times, "is this the right stop?" |
| 14 | Phone and messages | "Sorry, I can't hear you" |
| 15 | Weekend plans | Inviting, saying yes, saying no kindly |
| 16 | Weather and seasons | The weather is the safest small talk there is |
| 17 | Cooking at home | Steps, taste, admitting it failed |
| 18 | Money and prices | Asking the price, splitting the bill |
| 19 | Health and body | Saying what is wrong, seeing a doctor |
| 20 | Housing and rent | Looking at a place, describing problems |
| 21 | Travel and places | Stations, tickets, going somewhere new |
| 22 | Likes and dislikes | Giving an opinion without sounding rude |
| 23 | Agreeing and disagreeing | Saying no kindly, partly agreeing |
| 24 | Asking for help | Asking a stranger, politely but firmly |
| 25 | Losing your way | Admitting you are lost and getting out of it |
| 26 | Warnings and caution | Giving advice, saying no to someone |
| 27 | Workplace small talk | The bridge back to Days 1-10 |
| 28 | Hobbies and interests | What you do for fun |
| 29 | Storytelling | "One time..." — telling about your life |
| 30 | Sounding natural | Fillers, rhythm, the final exam |

**All 30 days are written.** Days 1-10 are workplace English, 11-26 everyday
conversation, and 27-30 fluency and storytelling. Days 11-26 were written one day
at a time after twelve parallel subagents produced nothing; each day's audio then
takes about two minutes to generate:

```bash
python scripts/audit_lessons.py          # what's written, and its shape
bash scripts/build_all_audio.sh 14       # generate one day's audio
```

Every day is 5 conversations and 1 long story, each with a matching MP3 — an
interviewer-only recording of the partner's lines, with a pause for you to answer
out loud.

**Day 30 is the one that changes everything.** By then you have 30 days of material
behind you, and the lesson is what native speakers actually do: pause, re-start,
say *"I mean..."*, laugh at yourself, and keep going. Fluency is not perfect
grammar. It is not stopping.