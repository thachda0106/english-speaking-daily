# Day 6 · Conversation 3 — The Root Cause

## 🎬 Situation
The manager wants the cause, and the whole team is in the meeting. The skill: say what changed, why that made the system slow, and prove it with a number you measured. A good cause fits in two sentences.

## 🗣️ Dialogue — read out loud (both roles), then play the audio and answer

> **Manager:** Tell the team the cause. Keep it simple.

> **You:** We deployed the new version at five in the afternoon. The new version changed one query in the report service.

> **Manager:** Which query? What changed in it?

> **You:** The query on the report table. Before, it read the data by customer id. Now it reads the whole table, and there is no index on the date column.

> **Manager:** And that is why it is slow?

> **You:** Yes. Without the index, the database checks row by row. The table has eight million rows, so one request takes eleven seconds. With the index it is twenty milliseconds.

> **Manager:** That is five hundred times faster. Good. Why did we not see this in the test?

> **You:** The test data is small — only two hundred rows. On two hundred rows the query is fast, so the test passed. In production it was eight million rows.

> **Manager:** Thank you. That is a clear answer. Please write it in the ticket and send it to the team.

> **You:** I will do it now.

## 🧠 Your active vocabulary — all words you already know
`deployed · new version · query · report service · report table · customer id · whole table · index · date column · row by row · eight million rows · request · eleven seconds · twenty milliseconds · test data · two hundred rows · production · ticket · team · cause · clear answer`

## ✅ After you speak
- The cause formula = **what we changed + why it is slow + the number that proves it**:
  *"We deployed the new version at five. It changed one query — the query now reads the whole table with no index. Eight million rows, eleven seconds, versus twenty milliseconds with the index."*
- 💡 **"root cause"** — the real reason, not the first error in the log. Say it: *"The root cause is the missing index on the date column."* One root cause per bug — if you list five, you have no answer.
- 💡 **"Why did we not see this in the test?"** — expect this question every time. Answer it before they ask: small test data hides slow queries. This question is not an attack; it is a test of whether you understand your own bug.
- 🧠 **Your mental model:** your cause must be a **chain of three links**: change → mechanism → number. Deploy (change) → no index, so full table scan (mechanism) → 11 seconds vs 20 ms (number). If one link is missing, the manager cannot repeat your explanation to the customer — and that is exactly why he needs it.
- 🎙️ Play `manager-03` and answer. Then explain the cause of a REAL bug you have fixed, using the three links, in under 30 seconds.

## ✅ Done when…
- [ ] I said what we changed, why it made the system slow, and the measured number
- [ ] I answered "why did the test not catch it?" without being asked twice
