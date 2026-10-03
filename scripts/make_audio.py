"""
Generate speaking-practice MP3s for one day folder.

Input shapes
------------
conversation-NN-slug.md
    Only the OTHER person's lines are read (the learner's "You:" lines are
    skipped). A long pause follows each line so the learner can answer out loud.

story-01-the-long-story.md
    The full narrative is read sentence by sentence with short pauses, for
    shadowing practice.

Each line is synthesized separately, then the parts are joined with real
silence. Synthesizing per line also means a rate/voice change only requires a
re-run of this script, not manual re-timing.

Usage
-----
  python scripts/make_audio.py day-06-explaining-a-bug
  python scripts/make_audio.py day-06-explaining-a-bug --voice en-US-GuyNeural --rate -10%
"""

import argparse
import asyncio
import io
import pathlib
import re
import subprocess
import sys

import edge_tts
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Pause AFTER each chunk, in milliseconds.
PAUSE_LINE = 2600        # conversation: room for the learner to answer
PAUSE_SENTENCE = 650     # story: natural breath between sentences

LINE_RE = re.compile(r"^>\s*\*\*(.+?):\*\*\s*(.+?)\s*$")
LEARNER_LABELS = {"you"}

# Strip markdown emphasis before speaking so TTS does not read the asterisks.
MD_RE = re.compile(r"[*_`]")


def clean(text: str) -> str:
    text = MD_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_conversation(path: pathlib.Path):
    """[(text, pause_after_ms)] for the other speaker only."""
    chunks = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(raw.strip())
        if not m:
            continue
        speaker, text = m.group(1).strip(), clean(m.group(2))
        if speaker.lower() in LEARNER_LABELS or not text:
            continue
        for piece in split_for_tts(text):
            chunks.append((piece, PAUSE_LINE))
    return chunks


def parse_story(path: pathlib.Path):
    """Story prose as sentences, skipping headings, quotes and checklists."""
    body, buf = [], []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        starts_block = (
            line.startswith("#")
            or line.startswith("---")
            or line.startswith(">")
            or line.startswith("- [ ]")
            or line.startswith("- **")
        )
        if starts_block:
            buf = []
            continue
        if not line:
            # Paragraph break: keep the collected text.
            if buf:
                body.append(clean(" ".join(buf)))
                buf = []
            continue
        buf.append(line)
    if buf:
        body.append(clean(" ".join(buf)))

    chunks = []
    for para in body:
        for sentence in re.split(r"(?<=[.!?])\s+", para):
            sentence = clean(sentence)
            if not sentence:
                continue
            for piece in split_for_tts(sentence):
                chunks.append((piece, PAUSE_SENTENCE))
    return chunks


def split_for_tts(text: str, limit: int = 230):
    """edge-tts drops very long inputs, so break on clause boundaries."""
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for piece in re.split(r"(?<=[,;:])\s+", text):
        if cur and len(cur) + len(piece) + 1 > limit:
            parts.append(cur)
            cur = piece
        else:
            cur = f"{cur} {piece}".strip()
    if cur:
        parts.append(cur)
    return parts


async def synth_chunk(text: str, voice: str, rate: str) -> bytes:
    """Stream one chunk to mp3 bytes. save() only accepts a path, so collect the
    audio payloads from the stream directly."""
    comm = edge_tts.Communicate(text, voice, rate=rate)
    buf = bytearray()
    async for item in comm.stream():
        if item["type"] == "audio":
            buf.extend(item["data"])
    if not buf:
        raise RuntimeError(f"edge-tts returned no audio for: {text[:60]!r}")
    return bytes(buf)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"{pathlib.Path(cmd[0]).name} failed:\n{r.stderr.decode()[:600]}"
        )


async def build(chunks, voice, rate, out_path: pathlib.Path):
    """Synthesize every chunk, lay real silence between them, then join.

    The final join re-encodes to one fixed mp3 format because edge-tts output
    and the generated silence do not share identical stream headers, and the
    concat demuxer cannot copy streams across mismatched containers cleanly.

    Temp parts are removed in a finally block: a failed run must not leave
    _tts_* files behind in the day's audio folder.
    """
    parts, tmp = [], []
    try:
        for i, (text, pause) in enumerate(chunks):
            data = await synth_chunk(text, voice, rate)
            p = out_path.parent / f"_tts_p{i:03d}.mp3"
            p.write_bytes(data)
            parts.append(p)
            tmp.append(p)

            if i < len(chunks) - 1 and pause:
                sp = out_path.parent / f"_tts_s{i:03d}.mp3"
                run([FFMPEG, "-y", "-f", "lavfi", "-i",
                     "anullsrc=channel_layout=mono:sample_rate=24000",
                     "-t", f"{pause / 1000}", "-c:a", "libmp3lame", "-b:a",
                     "48k", "-ar", "24000", "-ac", "1", str(sp)])
                parts.append(sp)
                tmp.append(sp)

        listfile = out_path.parent / f"_tts_list_{out_path.stem}.txt"
        # The concat demuxer requires "file '<path>'" lines, not bare paths.
        listfile.write_text(
            "\n".join(f"file '{p.name}'" for p in parts), encoding="utf-8"
        )
        tmp.append(listfile)
        run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
             "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
             str(out_path)])
    finally:
        for p in tmp:
            pathlib.Path(p).unlink(missing_ok=True)


def duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        [FFMPEG, "-i", str(path)], capture_output=True, text=True
    )
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return 0.0
    h, mnt, s = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(s)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("day")
    ap.add_argument("--voice", default="en-US-AriaNeural")
    ap.add_argument("--rate", default="-8%")
    ap.add_argument(
        "--prefix",
        required=True,
        help="speaker noun used for audio filenames, e.g. 'colleague' turns "
             "conversation-01-x.md into colleague-01-x.mp3",
    )
    args = ap.parse_args()

    day_dir = pathlib.Path(args.day)
    if not day_dir.is_dir():
        print(f"day folder not found: {day_dir}", file=sys.stderr)
        sys.exit(2)
    audio_dir = day_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    for md in sorted(day_dir.glob("*.md")):
        if md.name.startswith("conversation-"):
            chunks = parse_conversation(md)
            kind = "conv"
            name = f"{args.prefix}-{md.stem[len('conversation-'):]}.mp3"
        elif md.name.startswith("story-"):
            chunks = parse_story(md)
            kind = "story"
            # Stories are narrations, not a second speaker: keep the story- prefix.
            name = f"{md.stem}.mp3"
        else:
            continue
        if not chunks:
            print(f"  !! {md.name}: nothing to read")
            continue
        out = audio_dir / name
        await build(chunks, args.voice, args.rate, out)
        print(f"  ok  {out.as_posix():<62} {duration(out):6.1f}s  "
              f"{len(chunks):>3} chunks ({kind})")


if __name__ == "__main__":
    asyncio.run(main())
