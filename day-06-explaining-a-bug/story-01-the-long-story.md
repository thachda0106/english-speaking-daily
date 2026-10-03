# Day 6 · 📖 The Long Story — A Day When a Bug Broke Everything

> Today's long story is a real incident: alert → panic → investigation → hard decision → fix → prevention. It trains connected speech with **times, numbers and technical detail** — the exact things you must say out loud when a manager asks *"what happened?"*

---

**Tuesday was not a normal day for me — at ten in the morning, my phone rang, and it did not stop.**

The morning started normally. I opened my laptop at half past eight and drank my coffee. Duy, my teammate, told me about a new report page we wanted to add. I was working on the orders table, because our queries on that table were getting slower every week. I wanted to add an index on the customer column.

At ten o'clock, the alert came to our team chat. The report page was slow. Our monitor showed that ninety-five percent of the requests were taking more than ten seconds. Before that, they took four hundred milliseconds. Something was wrong, and it was not a little slow — it was very slow.

My manager called me. "Thach, I got the alert. The report page is slow. What happened?" I said, "I'm looking now. It started ten minutes ago." It was the first time I explained a bug to a manager in English, and my hands were cold.

I looked at the logs of the report API and saw a lot of timeouts. The server was fine — the CPU was at thirty percent, and the memory was fine too. So the problem was not the server. I checked the database, because a slow page with a healthy server usually means a slow query. I ran the query on the production database, and it took eleven seconds. On my local database it took twenty milliseconds.

Then I found the cause. We deployed version 1.4.0 at five in the afternoon, the day before. That version changed the report query. The old query looked for one customer, but the new query looked at the whole table — eight million rows. There was no index on this column, so the database read every row, one by one.

I asked myself the hard question: roll back, or fix it now? Duy said, "Go back to the old version first. Then fix it." He was right. At twenty past ten I started the rollback to version 1.3.5. It took four minutes. At twenty-four minutes past ten the page was fast again, so our users had a slow page for about thirty-four minutes.

Then I told my manager. "The bug is fixed. The cause is our new version — it changed the report query, and there is no index on the column. Between ten and twenty past ten, about nine hundred users had a slow page. No data was wrong." He asked me two questions and I answered both. He said, "Thank you. That's a clear explanation."

In the afternoon I added the index. It took twenty-two minutes on eight million rows, and after that the query took eighteen milliseconds. At eight tonight, when the traffic was low, we deployed version 1.4.1 with the fix. The monitor stayed green all night.

After that, I wrote down three things so this cannot happen again: a test with one million rows, a slow-query alert in the monitor, and no deploy at five in the afternoon. I also learned something about myself. I was afraid to speak, but the manager did not need perfect English. He needed three things: the cause, the numbers, and the fix. When I gave him those, he understood everything.

---

## 🧠 Story vocabulary & grammar
- **Past-tense verbs you just heard/read:** `was · started · opened · drank · told · wanted · got · came · showed · said · was looking · checked · saw · ran · took · found · deployed · changed · had to read · went back · wrote · learned`
- These are the irregular past forms you need for any story about a real day. Notice the pairs: say→said, find→found, run→ran, take→took, write→wrote, drink→drank. Keep the numbers short when you speak — say "eleven seconds", not "eleven point zero seconds" — the story stays clear at natural speed.

## ✅ Done when…
- [ ] I read the story out loud twice
- [ ] I shadowed the story audio (listened + repeated line by line)
- [ ] I retold the story in my own words in 60 seconds (no reading)
