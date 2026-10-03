"""The one place that knows which day exists and who speaks in its audio.

scripts/make_audio.py needs the speaker to name the mp3s. The test suite needs
the same value to know what to expect — and when those two lists drift, a day
silently produces audio under the wrong name.

So there is one list, here, and scripts/test_make_audio.py checks that every
day-XX-* folder in the repo appears in it. Adding a day without adding it here
is a test failure, not a mystery.

Speaker is the partner who talks in that day's audio. Conversations are named
for them; stories keep their story- name because nobody else speaks a story.
"""

DAYS = {
    # Days 1-4 predate this script; their audio was hand-made and two slugs
    # were shortened, so those are recorded rather than regenerated.
    "day-01-job-interview": "interviewer",
    "day-02-phone-screen": "recruiter",
    "day-03-new-team": "team",
    "day-04-daily-standup": "standup",
    # Days 5-10: workplace English.
    "day-05-code-review": "colleague",
    "day-06-explaining-a-bug": "manager",
    "day-07-salary-discussion": "recruiter",
    "day-08-negotiating-a-deadline": "manager",
    "day-09-small-talk-at-lunch": "colleague",
    "day-10-technical-interview": "interviewer",
    # Days 11-26 and 28-30: everyday conversational English with a friend.
    "day-11-coffee-shop": "friend",
    "day-12-grocery-shopping": "friend",
    "day-13-taking-a-bus": "friend",
    "day-14-phone-and-messages": "friend",
    "day-15-weekend-plans": "friend",
    "day-16-weather-and-seasons": "friend",
    "day-17-cooking-at-home": "friend",
    "day-18-money-and-prices": "friend",
    "day-19-health-and-body": "friend",
    "day-20-housing-and-rent": "friend",
    "day-21-travel-and-places": "friend",
    "day-22-likes-and-dislikes": "friend",
    "day-23-agreeing-and-disagreeing": "friend",
    "day-24-asking-for-help": "friend",
    "day-25-losing-your-way": "friend",
    "day-26-warnings-and-caution": "friend",
    # Day 27 is the bridge back to workplace English.
    "day-27-workplace-small-talk": "colleague",
    "day-28-hobbies-and-interests": "friend",
    "day-29-storytelling-past-experiences": "friend",
    "day-30-sounding-natural": "friend",
}

# Hand-made audio whose slug differs from the lesson filename. Keyed by
# (day, conversation number) -> the slug the mp3 actually uses.
LEGACY_SLUGS = {
    ("day-02-phone-screen", "04"): "salary",
    ("day-04-daily-standup", "01"): "the-format",
}


def mp3_for(day_folder: str, lesson_stem: str) -> str:
    """The mp3 filename a lesson should have.

    day_folder is the folder name ('day-07-salary-discussion'), lesson_stem is
    the .md filename without its extension.
    """
    if lesson_stem.startswith("story-"):
        return f"{lesson_stem}.mp3"
    number, slug = lesson_stem[len("conversation-"):].split("-", 1)
    slug = LEGACY_SLUGS.get((day_folder, number), slug)
    return f"{DAYS[day_folder]}-{number}-{slug}.mp3"