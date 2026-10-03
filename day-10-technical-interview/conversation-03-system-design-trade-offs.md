# Day 10 · Conversation 3 — System Design: Explaining a Trade-off

## 🎬 Situation
They ask: *"How would you design this?"* You will not build it. They only want to see **how you think out loud**. The skill is naming **trade-offs** — every choice costs something, and admitting that is the mark of seniority.

## 🗣️ Dialogue — read out loud (both roles), then play the audio and answer

> **Interviewer:** If you needed to make one of our APIs much faster, how would you approach it?

> **You:** It depends on where the time is going, so I'd measure first. I'd look at the logs and the database to find the slowest part.

> **Interviewer:** Okay, and if the database is the problem?

> **You:** There are two or three options. I could add an index, which is simple and low risk. I could add a cache, which is faster but the data might be old for a short time. Or I could read from a copy of the data that's only used for reading.

> **Interviewer:** How would you choose?

> **You:** I'd start with the index, because it's the cheapest and safest. I'd only add a cache if I measured that the query was still slow.

> **Interviewer:** That makes sense. What if the traffic grows ten times?

> **You:** Then I'd look at scaling the database first, and maybe put a cache in front. I'd want numbers before I changed the architecture.

## 🧠 Your active vocabulary — all words you already know
`approach · faster · where · going · measure · logs · database · slowest · options · add · index · simple · low risk · cache · data might be old · copy · reading · choose · start · cheapest · safest · measured · traffic · grows · ten times · scaling · front · numbers · changed · architecture`

## ✅ After you speak
- The system-design formula = **measure → give options → pick the safe one first → say what would change it**:
  *"I'd measure first. Then the options are: add an index, add a cache, or read from a copy. I'd start with the index, because it's the cheapest and safest."*
- 💡 **"It depends on where the time is going."** — the most senior sentence in this whole dialogue. It says: I don't guess, I measure. 💡 **Never start a design answer with a technology.** Start with the question you need to answer.
- 💡 **"Which is faster but the data might be old."** — naming the **cost** of your choice out loud is what interviewers are listening for. A cache is not free; it trades freshness for speed. Say the cost, every time.
- 💡 **"I'd want numbers before I changed the architecture."** — pure senior thinking. Architecture decisions are expensive to undo, so you want evidence first.
- 🎙️ Play `interviewer-03` and answer. **Today: say this dialogue out loud twice. You already know this material — it's your caching and scaling roadmap, just in English.**
- 🧠 **Your mental model:** you already studied this. Cache-Control, ETag, CDN, Vary, distributed cache, invalidation — that's Day 4 of your caching series, and the scaling road from your system design practice. **This conversation is that knowledge with an English accent.** The content is done. Only the delivery is new.

## ✅ Done when…
- [ ] I said "It depends on where the time is going"
- [ ] I named 2-3 options and said why I picked the safe one first
- [ ] I named the cost of my choice
