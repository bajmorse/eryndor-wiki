#!/usr/bin/env python3
"""Transcribe a Craig multitrack recording into one speaker-labelled transcript.

Craig exports one time-aligned FLAC per Discord user (``N-username.flac``), all
padded to the same length. Transcribing each track on its own gives exact
speaker attribution for free, so we do that, then merge the per-track segments
by timestamp into a single transcript.

Per-track progress is written to ``<out>/tracks/<username>.jsonl`` as it goes,
so an interrupted run can be resumed by running the same command again.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

TRACK_RE = re.compile(r"^\d+-(.+)\.flac$")


def hms(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def load_json(path: Path, default):
    if path and path.exists():
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    return default


def preflight(flac: Path):
    """Decode one frame before the model loads, so a broken audio stack fails
    in seconds rather than after a multi-minute model load.

    Mirrors the exact av.open() call faster_whisper/audio.py makes, so it trips
    on the same incompatibilities (see the version pins in the Dockerfile).
    """
    try:
        import av
    except Exception as e:  # pragma: no cover - import guard
        sys.exit(f"PyAV import failed: {e}")
    try:
        with av.open(str(flac), mode="r", metadata_errors="ignore") as container:
            next(container.decode(audio=0))
    except TypeError as e:
        sys.exit(
            f"PyAV {getattr(av, '__version__', '?')} is incompatible with this "
            f"faster-whisper ({e}).\n"
            "Fix the pins in tools/transcribe/Dockerfile (needs av<19) and rebuild."
        )
    except Exception as e:
        sys.exit(f"could not decode {flac.name}: {type(e).__name__}: {e}")


def transcribe_track(model, flac: Path, out_jsonl: Path, vocab: str, beam_size: int):
    """Run one track; write segments to out_jsonl. Returns segment count."""
    segments, info = model.transcribe(
        str(flac),
        language="en",
        beam_size=beam_size,
        vad_filter=True,
        vad_parameters={
            "min_silence_duration_ms": 700,
            "speech_pad_ms": 300,
        },
        # Each track is one voice with long gaps; carrying context across gaps
        # mostly causes repetition loops, not better output.
        condition_on_previous_text=False,
        initial_prompt=vocab or None,
    )
    duration = info.duration or 0
    count = 0
    started = time.time()
    last_report = 0.0
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            f.write(json.dumps({"start": seg.start, "end": seg.end, "text": text}) + "\n")
            f.flush()
            count += 1
            if seg.end - last_report >= 300 or last_report == 0:
                last_report = seg.end
                pct = (seg.end / duration * 100) if duration else 0
                elapsed = time.time() - started
                print(
                    f"  {flac.name}: {hms(seg.end)} / {hms(duration)} ({pct:4.1f}%)  "
                    f"{count} segments, {hms(elapsed)} elapsed",
                    flush=True,
                )
    print(f"  {flac.name}: done, {count} segments in {hms(time.time() - started)}", flush=True)
    return count


def merge(tracks_dir: Path, speakers: dict, out_dir: Path, gap: float):
    """Merge all per-track jsonl files into transcript.md / transcript.json."""
    rows = []
    for jsonl in sorted(tracks_dir.glob("*.jsonl")):
        user = jsonl.stem
        label = speakers.get(user, user)
        with jsonl.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                d["speaker"] = label
                d["user"] = user
                rows.append(d)
    rows.sort(key=lambda r: r["start"])

    # Fold runs of consecutive segments from the same speaker into one
    # paragraph when the pause between them is short.
    merged = []
    for r in rows:
        if merged and merged[-1]["speaker"] == r["speaker"] and r["start"] - merged[-1]["end"] <= gap:
            merged[-1]["end"] = r["end"]
            merged[-1]["text"] += " " + r["text"]
        else:
            merged.append(dict(r))

    with (out_dir / "transcript.json").open("w", encoding="utf-8") as f:
        json.dump(merged, f, indent=1)
    with (out_dir / "transcript.md").open("w", encoding="utf-8") as f:
        f.write("# Session transcript\n\n")
        f.write("Auto-transcribed (faster-whisper) from Craig multitrack tracks; "
                "speaker labels come from the track, timestamps are session-relative.\n\n")
        for r in merged:
            f.write(f"**[{hms(r['start'])}] {r['speaker']}:** {r['text']}\n\n")
    print(f"Merged {len(rows)} segments into {len(merged)} turns -> {out_dir / 'transcript.md'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, type=Path, help="directory containing N-username.flac tracks")
    ap.add_argument("--output", required=True, type=Path, help="directory for tracks/*.jsonl and transcript.*")
    ap.add_argument("--model", default=os.environ.get("MODEL", "large-v3"),
                    help="faster-whisper model name (large-v3, large-v3-turbo, medium.en, ...)")
    ap.add_argument("--compute-type", default=os.environ.get("COMPUTE_TYPE", "int8"))
    ap.add_argument("--threads", type=int, default=int(os.environ.get("THREADS", os.cpu_count() or 4)))
    ap.add_argument("--beam-size", type=int, default=int(os.environ.get("BEAM_SIZE", 5)))
    ap.add_argument("--speakers", type=Path, default=Path(__file__).with_name("speakers.json"))
    ap.add_argument("--vocab", type=Path, default=Path(__file__).with_name("vocab.txt"))
    ap.add_argument("--merge-gap", type=float, default=2.0,
                    help="seconds of silence allowed between same-speaker segments folded into one turn")
    ap.add_argument("--merge-only", action="store_true", help="skip transcription; just rebuild transcript.*")
    args = ap.parse_args()

    speakers = {k: v for k, v in load_json(args.speakers, {}).items() if not k.startswith("_")}
    vocab = args.vocab.read_text(encoding="utf-8").strip() if args.vocab.exists() else ""
    tracks_dir = args.output / "tracks"
    args.output.mkdir(parents=True, exist_ok=True)

    if not args.merge_only:
        tracks = sorted(p for p in args.input.iterdir() if TRACK_RE.match(p.name))
        if not tracks:
            sys.exit(f"no N-username.flac tracks found in {args.input}")
        preflight(tracks[0])
        print(f"Model {args.model} ({args.compute_type}, {args.threads} threads); {len(tracks)} tracks", flush=True)

        from faster_whisper import WhisperModel
        model = WhisperModel(args.model, device="cpu", compute_type=args.compute_type, cpu_threads=args.threads)

        for flac in tracks:
            user = TRACK_RE.match(flac.name).group(1)
            out_jsonl = tracks_dir / f"{user}.jsonl"
            done_marker = tracks_dir / f"{user}.done"
            if done_marker.exists():
                print(f"Skipping {flac.name} (already transcribed)", flush=True)
                continue
            print(f"Transcribing {flac.name} as '{speakers.get(user, user)}'", flush=True)
            transcribe_track(model, flac, out_jsonl, vocab, args.beam_size)
            done_marker.touch()

    merge(tracks_dir, speakers, args.output, args.merge_gap)


if __name__ == "__main__":
    main()
