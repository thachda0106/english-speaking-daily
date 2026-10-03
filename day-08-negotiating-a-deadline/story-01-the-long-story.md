# Day 8 · 📖 The Long Story — The Deadline I Pushed Back On

> This story is the anchor of Day 8: one long narrative in the past tense, full of **hedging and modals** — *I don't think…*, *it would take…*, *could we…?* Read it out loud twice, shadow the audio, then retell it in your own words.

---

**Monday was the day my manager gave me a deadline I did not believe, and I almost said yes without asking a single question.**

It started at the morning stand-up. A customer wanted a report feature: download all your orders as a file, with a filter by month. My manager said we should finish it by Friday — four working days away. Duy, my teammate, said quietly after the meeting that Friday sounded fast.

I felt bad in my chest. I was two months into the job, and I did not want to be the new person who says no too early. So I said nothing. I opened the code and read it. I looked at the migration we would need, because the order data lives in three tables. I checked the tests — there were none.

I wrote a list. Reading the code and planning the query: one day. The migration on the big orders table: two days, because we can only run it at night. Tests, because the service has none: one day. The export itself: two days. That made six days — and I was not sure about the old data yet.

So I did not go to my manager with a problem. I went with questions. I asked Duy first, because he knows this system. "How often do we run a migration like this?" "Every two months, and it takes a whole night." I asked if we could build the report without the migration. He said yes, but the query would be slow. That was not in the original task.

On Tuesday I went to my manager. "I read the code and I made a list. I don't think we can finish the full task by Friday. I think we can finish a first version." Then I gave him three options. One: do the export only. Two: add one more person. Three: move the date one week. I did not say "this is impossible." I said what I saw in the code.

My manager was not happy at first. He said the date could not move: the customer was waiting, and sales had already promised it. I was afraid, but I did not argue. "Could we check one thing — how important is this report for the customer?" We read the tickets. The customer only needed a file for the last three months. Everything else was our own idea.

We agreed on this. I would build the export with one filter, no email, no second file format. Duy would do the migration in the second week. We would check on Wednesday. And if it was slow, I would tell him on Monday — not Thursday night.

I finished the first version on Wednesday morning, two days early. The query was slow, but I added an index and the tests passed. Duy found only two small problems. The manager sent the file to the customer on Thursday, and the customer was happy.

After that day I understood something simple. I did not fail anything. I only moved some work to the next week, out loud, in a meeting, in English, with three options on the table. Speaking up early is cheap. Failing late is expensive. My fear was never the deadline — it was saying no. And saying no is a skill.

---

## 🧠 Story vocabulary & grammar
- **Past-tense verbs you just heard/read:** `said · told · read · looked · checked · wrote · added · asked · went · gave · understood · agreed · built · ran · found · finished · passed · sent · felt · practised · was`
- **Modals and hedging are the real grammar of this day.** Compare: *"We can do it by Friday"* (a promise you may not keep) → *"I don't think we can do it by Friday"* (an opinion) → *"It would take about six days"* (a soft number) → *"Could we do the first part on Friday and the rest next week?"* (a question that gives the other person two easy ways to say yes). Hedging is not weakness — it is how you keep a promise you can actually keep.
- Notice "I did not want to be the new person who says no too early." Simple past + clause — no nervous present tense. Past tense keeps the story steady, like a service that is healthy.

## ✅ Done when…
- [ ] I read the story out loud twice
- [ ] I shadowed the story audio (listened + repeated line by line)
- [ ] I retold the story in my own words in 60 seconds (no reading)
