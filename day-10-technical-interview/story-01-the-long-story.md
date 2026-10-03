# Day 10 · 📖 The Long Story — The Interview I Almost Failed

> The last day, and one long story. Read it out loud twice, shadow the audio, then retell it in your own words. It ties the whole course together — because in a real interview you use **everything at once**: numbers, structure, honesty, and questions.

---

**Last Tuesday I had a technical interview, and at the end I almost did not get the job because of one small sentence I said at the beginning.**

I had been preparing for weeks. I reviewed my projects, I read about system design, and I practised my English out loud in the morning. Still, I was nervous the whole morning of the interview. I checked my camera and my microphone three times.

The interviewer introduced himself and asked, "So, can you tell me a little about your background?" This was the question I had practised most. I said, "I'm a backend engineer with about four years of experience, mostly with Node.js and TypeScript. I work with PostgreSQL, and I've spent a lot of time on performance — slow queries, indexes, and caching." Then I stopped, because I was afraid I had said too much.

Then he asked, "What kind of projects have you worked on?" I said, "Mostly e-commerce and task management systems. Right now I work on a system that handles thousands of requests every minute, so I think reliability is a big part of my job." He said, "That sounds relevant to us," and then he asked the question I was waiting for: "What would you like to focus on today?"

I did not say "whatever you want." I said, "I'd be happy to talk about how I found and fixed a production performance problem."

I walked him through it. The API was slow — about five hundred milliseconds, sometimes three seconds. I looked at the logs and saw the slow requests were all the same query. I checked the execution plan, and there was no index on the column we were filtering by. I added the index, and I changed the query to select only the columns we needed. The response time went down to about forty milliseconds. I ran the tests first, and I watched the database for a day. Memory use stayed the same.

He asked, "How would you make it faster in general?" I said I would measure first, and then I gave him my options: add an index, add a cache, or read from a copy of the data. I told him I would start with the index, because it was the cheapest and the safest, and I would only add a cache if the query was still slow after that. He said, "That makes sense."

Then he asked about Kafka, and honestly, I have never used it in real work. I said, "I've only read about it. I know the general idea, but I haven't used it yet." He looked at me for a second and said, "That's better than guessing." Then I said the sentence I had practised: when I joined my company, I had to learn a system I had never used, and I learned it in a few weeks — read first, then build something small, then get feedback from the team. He wrote something down.

At the end, he asked if I had any questions. Ten days ago, I would have said no. Instead I said, "What does the team look like right now?" and then, "For this role, what would you want me to be good at after six months?" He said he would want me to own a whole feature, including the database design. I said, "That sounds like a good challenge."

On the train home, I was tired and I kept thinking about my first sentence. I had worried it was too simple. But then I understood something. The interview was not a test of how much English I know. It was a test of whether I can think clearly and say it out loud. And for that, the words were never the problem. The problem was fear — and fear is just a habit, and habits can be trained, like anything else.

---

## 🧠 Story vocabulary & grammar
- **Past-tense verbs you just read:** `was · had · introduced · asked · said · spent · stopped · walked · went · saw · checked · added · changed · ran · watched · stayed · looked · wrote · thought · understood · kept · wanted · gave · trained`
- Notice the **conditional and hedging** hiding in there: *"It was slow — about five hundred milliseconds."* *"I would start with the index."* *"If the query was still slow."* This is how senior engineers sound precise: they never say a bare number or a bare fact, they always attach a condition to it.
- Also notice: **"He said, '…'"** — past tense for reported speech. The interviewer's words are in the past, but the words themselves stay in the present. That's why *"He said, 'Do you have any questions?'"* and not *"He said, 'Did you have any questions?'"*

## ✅ Done when…
- [ ] I read the story out loud twice
- [ ] I shadowed the story audio (listened + repeated line by line)
- [ ] I retold the story in my own words in 60 seconds (no reading)
- [ ] I can say all 8 items in the interview toolkit from Day 10, Conversation 5
