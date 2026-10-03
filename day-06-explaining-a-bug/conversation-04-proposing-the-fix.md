# Day 6 · Conversation 4 — Proposing the Fix

## 🎬 Situation
The cause is clear, but the page is still slow and users are waiting. You have two options: go back to the old version now, or fix it properly. The skill: give both options with a time for each, and recommend one.

## 🗣️ Dialogue — read out loud (both roles), then play the audio and answer

> **Manager:** Okay, you found the cause. What do we do now?

> **You:** I can go back to the old version in five minutes. That stops the slow query now, but the cause stays in the code.

> **Manager:** And the real fix?

> **You:** Add the index on the date column. The index will take about twenty minutes to build, because the table has eight million rows. After that the query is twenty milliseconds.

> **Manager:** Twenty minutes is a long time for users. Can we do both?

> **You:** Yes. I go back to the old version now, and I build the index tonight when the traffic is low.

> **Manager:** Is it safe to build the index on the production database?

> **You:** Yes, the database can work while the index is building. The old version reads by customer id, so it does not need the new index.

> **Manager:** Good. Go back to the old version first, and I want a message when the page is normal.

> **You:** I will do it now. I will send you a message in five minutes with the result.

## 🧠 Your active vocabulary — all words you already know
`cause · old version · minutes · slow query · code · fix · index · date column · build · eight million rows · real fix · users · both · traffic · low · safe · production database · page · normal · result · message · send`

## ✅ After you speak
- The propose-the-fix formula = **fast option now + real fix later + my recommendation**:
  *"I can go back to the old version in five minutes — that stops it now but the cause stays. The real fix is the index, twenty minutes to build. I'd go back now and build the index tonight."*
- 💡 **"rollback"** = going back to the version that worked before. Say it: *"I started the rollback at ten twenty."* After you learn the word once, every engineer in every meeting will use it.
- 💡 **"Can we do both?"** — the question that saves you from choosing between fast and correct. Always ask it. The answer is usually yes.
- 🧠 **Your mental model:** this is the same trade-off you already reason about in code — **fast mitigation vs. correct fix**, and you can do both because they touch different things. The rollback changes *which code runs*; the index changes *the database*. That is why they do not conflict.
- 🎙️ Play `manager-04` and answer. Then write a REAL proposal for a bug you fixed: fast option + real fix + your recommendation, three sentences, out loud.

## ✅ Done when…
- [ ] I gave both options with a time for each
- [ ] I recommended one and said why, instead of only listing
