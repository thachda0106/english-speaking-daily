# Day 10 · Conversation 2 — Explaining a Technical Problem Clearly

## 🎬 Situation
Now the real work. They ask about a technical problem and your only job is to **explain it clearly**. The skill is structure: **situation → problem → what I did → result.** No jargon dumps, no guessing.

## 🗣️ Dialogue — read out loud (both roles), then play the audio and answer

> **Interviewer:** Can you tell me about a difficult performance problem you solved?

> **You:** Sure. We had an API that became very slow under load — about five hundred milliseconds at the start, and sometimes three seconds.

> **Interviewer:** How did you find the cause?

> **You:** I looked at the logs first and saw the slow requests were all the same query. Then I checked the execution plan, and there was no index on the column we were filtering by.

> **Interviewer:** So what did you do?

> **You:** I added the index, and I also changed the query to only select the columns we needed. After that, the response time went down to about forty milliseconds.

> **Interviewer:** That's a big improvement. How did you make sure it was safe?

> **You:** I ran the test suite first, and I watched the database for a day after the change. Nothing went up — the memory use stayed the same.

## 🧠 Your active vocabulary — all words you already know
`difficult · performance · problem · API · slow · load · milliseconds · seconds · logs · requests · query · execution plan · index · column · filtering · added · select · response time · went down · improvement · safe · test suite · watched · memory use · stayed`

## ✅ After you speak
- The technical-explanation formula = **situation → how I found it → what I changed → result → safety**:
  *"It was slow at five hundred milliseconds. I looked at the logs and found one query. There was no index, so I added it. It went down to forty milliseconds, and the memory use stayed the same."*
- 💡 **"Let me walk you through it."** — the best opening for any technical answer. It tells the interviewer you have a structure. Use it.
- 💡 **"How did you find the cause?"** — 💡 always expect this. Measuring before fixing is the single thing that separates a senior engineer from a junior one. Never say "I just changed it."
- 💡 **"How did you make sure it was safe?"** — the question that tells them how you work in production. Always answer it, even if they don't ask.
- 🎙️ Play `interviewer-02` and answer. **Today: pick one real problem you solved and say it in the 4-part structure. Record it.**
- 🧠 **Your mental model:** you already know this story from real work — the query plan, the missing index, the memory check. **The English is the only new part.** You are not learning system design today. You are translating what you already have.

## ✅ Done when…
- [ ] I used all 4 parts (situation → find → change → result)
- [ ] I answered "how did you make sure it was safe?"

## 🔁 Your turn — fill this in out loud, do not read it

> *"Let me walk you through it. Last year we had an API that was slow under load — about ___ milliseconds, sometimes ___. I looked at the logs and saw the slow requests were one query. I checked the execution plan and there was no index on the column we filtered by. So I added the index, and I also changed the query to select only the columns we needed. After that, the response time went down to about ___. I ran the test suite first, and I watched the database for a day — memory use stayed the same."*

Now say it with your real numbers. 💡
