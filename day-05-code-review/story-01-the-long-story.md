# Day 5 · 📖 The Long Story — A Day of Code Review

> Every day now has **one long story** that tells the whole day as a continuous narrative. Read it out loud twice, shadow the audio, then retell it in your own words. It trains connected speech — the way you actually talk when someone asks *"how was your day?"*

---

**Friday was a big day for me — it was the day I finished my first feature at the new company.**

The morning started with the stand-up. I told my team that the fix was ready and that I had created a pull request. Duy, one of my teammates, said he would review it after lunch. I tried to keep the change small — about a hundred lines, plus some tests. Small changes are easier to review.

After lunch, the review came. Duy found a few small problems. The variable names in my new function were a bit confusing — names like "data" and "info" didn't tell us what they really held. That was fair. I agreed to fix the names and check the loop logic again.

Then there was a harder question. Why did I choose a new table instead of adding a column to the old one? I explained that the data had a different life cycle — it was born, used for a short time, and then deleted, while the old data lived forever. Duy saw my point, but he thought a column would be simpler. I didn't argue. I checked how the team usually handled this and followed their pattern. That day I learned something important: **the team's pattern matters more than my own idea.**

Duy also asked about the caching part. This time I was ready. I explained that the query runs very often and the data doesn't change much. And I had measured it — the cache made the response about three times faster. What about the memory cost? The cache holds only a thousand items, so the cost was low. Duy smiled and said it made sense.

At the end of the day, Duy approved the pull request. I merged the code, updated the task on the board, and closed the feature. It was my first merged feature at the company, and it felt great.

That night, I thought about the whole day. The code was good, but the best part was the talking — explaining my decisions, accepting feedback, and following the team's patterns. English was part of it now. It wasn't perfect, but it worked. And little by little, it was getting easier.

---

## 🧠 Story vocabulary & grammar
- **Past-tense verbs you just heard/read:** `said · told · created · found · agreed · explained · learned · measured · asked · smiled · approved · merged · closed · felt · thought · worked`
- These are the irregular past forms you need for ANY story about yesterday. Notice the pairs: say→said, tell→told, find→found, think→thought, feel→felt, teach→taught.

## ✅ Done when…
- [ ] I read the story out loud twice
- [ ] I shadowed the story audio (listened + repeated line by line)
- [ ] I retold the story in my own words in 60 seconds (no reading)
