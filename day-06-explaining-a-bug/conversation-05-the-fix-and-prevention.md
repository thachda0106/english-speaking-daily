# Day 6 · Conversation 5 — The Fix and Prevention

## 🎬 Situation
The page is normal again and the manager is calm. Now the most senior question: what will we do so it never happens again? The skill: say what changed in the system, then give one or two real prevention steps with a time.

## 🗣️ Dialogue — read out loud (both roles), then play the audio and answer

> **Manager:** Good, the page is normal now. What did you change?

> **You:** Two things. I started a new version with the index on the date column, and I changed the deploy time.

> **Manager:** What about the new version — how do we know the query is fast now?

> **You:** I checked with the monitor. The response is now under one second, and I also ran the query directly on the database. It takes twenty milliseconds.

> **Manager:** And how do we stop this from happening again?

> **You:** Two things. First, we do not deploy at five in the afternoon — we deploy in the morning. Second, we add a test that checks the query time on a big table.

> **Manager:** Can we test on big data in the test environment?

> **You:** Yes. We can copy one million rows into the test database and run the same query. It will show the slow query before we deploy.

> **Manager:** That is a good plan. Please write it in the ticket and check with Duy tomorrow.

> **You:** I will write it now. Thank you for helping me understand it.

## 🧠 Your active vocabulary — all words you already know
`page · normal · change · version · index · date column · deploy time · monitor · response · under one second · run · query · database · twenty milliseconds · morning · test · query time · big table · test environment · one million rows · copy · ticket · check · Duy · plan · tomorrow · thank you`

## ✅ After you speak
- The prevention formula = **what I changed + how we check + what stops it next time**:
  *"I deployed the version with the index — the response is under one second. To stop it, we deploy in the morning, not at five, and we add a test that checks the query time on a big table."*
- 💡 **"postmortem"** / **"retrospective"** — the meeting after an incident where the team asks *what went wrong, and what stops it happening again*. Say it once at work: *"I will send you the details for the retrospective."*
- 💡 **"How do we stop this from happening again?"** — the question every manager asks. Do not answer "I will be more careful." Answer with a **test**, an **alert**, or a **rule** — something in the system, not in your head.
- 🧠 **Your mental model:** a fix changes the code; prevention changes the **system**. Index = fix. Deploy-time rule + big-data query test = prevention. Most junior engineers stop at the fix — senior ones always finish the second half of the sentence.
- 🎙️ Play `manager-05` and answer. Then write the prevention part of a REAL incident you were part of — one test or one alert — in English, and send it to your team.

## ✅ Done when…
- [ ] I said what changed in the system, not just "I fixed the query"
- [ ] I gave a prevention step that lives in a test, an alert, or a team rule
