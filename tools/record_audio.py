# SPDX-License-Identifier: MIT
"""Record audio for the word list, one word at a time.

Reads a tab-separated word list with a header row that contains an `id`
column and a text column (default: `de`), shows one entry at a time, records
it from the microphone, trims the silence, evens out the loudness and saves
it as `<out>/<id>.mp3`. Entries that already have a file are skipped, so an
interrupted session simply continues where it stopped.

Setup (once, from the repository root):
    py -m venv .venv
    .venv\\Scripts\\python -m pip install -r tools\\requirements.txt

Usage:
    .venv\\Scripts\\python tools\\record_audio.py vocab\\pilot.tsv
    .venv\\Scripts\\python tools\\record_audio.py vocab\\pilot.tsv --redo mikro-urin
    .venv\\Scripts\\python tools\\record_audio.py vocab\\pilot.tsv --column uk --out audio\\uk
    .venv\\Scripts\\python tools\\record_audio.py --list-devices
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

FRAME_SECONDS = 0.01        # analysis frame for silence detection
SPEECH_BELOW_PEAK_DB = 35   # frames quieter than this below the loudest frame count as silence
MIN_SPEECH_DB = -50         # if even the loudest frame is below this, nothing was said
PAD_START_SECONDS = 0.10    # silence kept before the first sound
PAD_END_SECONDS = 0.20      # silence kept after the last sound
STOP_CLICK_SECONDS = 0.15   # cut from the end of a take: the Enter key that stopped it
FADE_SECONDS = 0.01         # fade in/out against clicks at the cut points
TARGET_RMS_DB = -20.0       # loudness of the spoken part after normalisation
MAX_PEAK_DB = -1.0          # never louder than this
CLIP_LEVEL = 0.99           # input peak at or above this means the take clipped


def db(value):
    return 20 * np.log10(max(value, 1e-12))


def read_word_list(path, column):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if not rows:
        sys.exit(f"{path}: no entries")
    for name in ("id", column):
        if name not in rows[0]:
            sys.exit(f"{path}: missing column '{name}' (found: {', '.join(rows[0])})")
    seen = set()
    for number, row in enumerate(rows, start=2):
        entry_id = (row["id"] or "").strip()
        if not ID_PATTERN.match(entry_id):
            sys.exit(f"{path}, line {number}: id '{entry_id}' may only contain A-Z, a-z, 0-9, _ and -")
        if entry_id in seen:
            sys.exit(f"{path}, line {number}: duplicate id '{entry_id}'")
        seen.add(entry_id)
    return [(row["id"].strip(), (row[column] or "").strip()) for row in rows]


def record_take(samplerate, device, channel):
    """Record from the moment this is called until the user presses Enter."""
    chunks = []

    def callback(indata, frames, time, status):
        chunks.append(indata[:, channel - 1].copy())

    with sd.InputStream(samplerate=samplerate, device=device, channels=channel,
                        dtype="float32", callback=callback):
        input("  ● Recording … Enter = stop")
    audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype="float32")
    return audio[: max(0, len(audio) - int(STOP_CLICK_SECONDS * samplerate))]


def trim_silence(audio, samplerate):
    """Cut leading and trailing silence. Returns None if no speech was found."""
    frame = int(FRAME_SECONDS * samplerate)
    count = len(audio) // frame
    if count == 0:
        return None
    frames = audio[: count * frame].reshape(count, frame)
    levels = 20 * np.log10(np.sqrt(np.mean(frames**2, axis=1)) + 1e-12)
    if levels.max() < MIN_SPEECH_DB:
        return None
    speech = np.flatnonzero(levels > levels.max() - SPEECH_BELOW_PEAK_DB)
    start = max(0, speech[0] * frame - int(PAD_START_SECONDS * samplerate))
    end = min(len(audio), (speech[-1] + 1) * frame + int(PAD_END_SECONDS * samplerate))
    trimmed = audio[start:end].copy()
    fade = min(int(FADE_SECONDS * samplerate), len(trimmed) // 2)
    if fade:
        ramp = np.linspace(0.0, 1.0, fade, dtype=trimmed.dtype)
        trimmed[:fade] *= ramp
        trimmed[-fade:] *= ramp[::-1]
    return trimmed


def normalise(audio, samplerate):
    """Scale the take so the spoken part has the target loudness, without clipping."""
    frame = int(FRAME_SECONDS * samplerate)
    count = max(1, len(audio) // frame)
    frames = audio[: count * frame].reshape(count, -1)
    rms = np.sqrt(np.mean(frames**2, axis=1))
    spoken = rms[20 * np.log10(rms + 1e-12) > db(rms.max()) - SPEECH_BELOW_PEAK_DB]
    gain = 10 ** ((TARGET_RMS_DB - db(np.sqrt(np.mean(spoken**2)))) / 20)
    peak = np.max(np.abs(audio)) * gain
    if peak > 10 ** (MAX_PEAK_DB / 20):
        gain *= 10 ** (MAX_PEAK_DB / 20) / peak
    return (audio * gain).astype("float32")


def process(raw, samplerate):
    """Turn a raw take into the file content. Returns (audio or None, warnings)."""
    warnings = []
    if len(raw) and np.max(np.abs(raw)) >= CLIP_LEVEL:
        warnings.append("The take clipped (too loud). Lower the input gain and redo it.")
    audio = trim_silence(raw - np.mean(raw) if len(raw) else raw, samplerate)
    if audio is None:
        return None, warnings + ["No speech detected. Check the microphone and the input channel."]
    if len(audio) / samplerate > 8:
        warnings.append("Longer than 8 s. Did the recording start too early or stop too late?")
    return normalise(audio, samplerate), warnings


def save_mp3(audio, samplerate, path):
    tmp = path.with_name(path.name + ".tmp")
    sf.write(tmp, audio, samplerate, format="MP3", subtype="MPEG_LAYER_III",
             bitrate_mode="VARIABLE", compression_level=0.2)
    os.replace(tmp, path)


def play(audio, samplerate):
    sd.play(audio, samplerate)
    sd.wait()


def record_entry(entry_id, text, position, total, out_dir, samplerate, device, channel):
    """Record one entry. Returns 'saved', 'skipped' or 'quit'."""
    print(f"\n[{position}/{total}] {entry_id}\n\n    {text}\n")
    answer = input("  Enter = start recording · s = skip · q = quit: ").strip().lower()
    if answer == "s":
        return "skipped"
    if answer == "q":
        return "quit"
    while True:
        audio, warnings = process(record_take(samplerate, device, channel), samplerate)
        for warning in warnings:
            print(f"  ! {warning}")
        if audio is not None:
            print(f"  ▶ {len(audio) / samplerate:.1f} s")
            play(audio, samplerate)
        prompt = "  Enter = keep · r = redo · p = play again · s = skip · q = quit: "
        if audio is None:
            prompt = "  r/Enter = redo · s = skip · q = quit: "
        while True:
            answer = input(prompt).strip().lower()
            if answer == "p" and audio is not None:
                play(audio, samplerate)
                continue
            break
        if answer == "" and audio is not None:
            save_mp3(audio, samplerate, out_dir / f"{entry_id}.mp3")
            print(f"  ✓ saved {out_dir / (entry_id + '.mp3')}")
            return "saved"
        if answer == "s":
            return "skipped"
        if answer == "q":
            return "quit"
        # "r", or Enter after a failed take: record again
        input("  Enter = start recording: ")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("wordlist", nargs="?", type=Path, help="tab-separated word list")
    parser.add_argument("--column", default="de", help="column with the text to read (default: de)")
    parser.add_argument("--out", type=Path, default=Path("audio/de"), help="output folder (default: audio/de)")
    parser.add_argument("--redo", nargs="+", metavar="ID", help="re-record these entries even if a file exists")
    parser.add_argument("--all", action="store_true", help="go through every entry, including recorded ones")
    parser.add_argument("--device", help="input device: number or part of its name (default: system default)")
    parser.add_argument("--channel", type=int, default=1, help="input channel on the device (default: 1)")
    parser.add_argument("--list-devices", action="store_true", help="show audio devices and exit")
    args = parser.parse_args()
    # A console handles Unicode anyway; a pipe or file on Windows would default to cp1252.
    if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.list_devices:
        print(sd.query_devices())
        return
    if args.wordlist is None:
        parser.error("the word list is required")

    device = int(args.device) if args.device and args.device.isdigit() else args.device
    samplerate = int(sd.query_devices(device, kind="input")["default_samplerate"])
    entries = read_word_list(args.wordlist, args.column)
    if args.redo:
        unknown = set(args.redo) - {entry_id for entry_id, _ in entries}
        if unknown:
            sys.exit(f"Not in the word list: {', '.join(sorted(unknown))}")
    args.out.mkdir(parents=True, exist_ok=True)

    def wanted(entry_id, text):
        if not text:
            return False
        if args.redo:
            return entry_id in args.redo
        return args.all or not (args.out / f"{entry_id}.mp3").exists()

    todo = [(entry_id, text) for entry_id, text in entries if wanted(entry_id, text)]
    print(f"{len(todo)} of {len(entries)} entries to record → {args.out}  "
          f"({sd.query_devices(device, kind='input')['name']}, channel {args.channel}, {samplerate} Hz)")

    counts = {"saved": 0, "skipped": 0}
    try:
        for position, (entry_id, text) in enumerate(todo, start=1):
            result = record_entry(entry_id, text, position, len(todo), args.out,
                                  samplerate, device, args.channel)
            if result == "quit":
                break
            counts[result] += 1
    except KeyboardInterrupt:
        print("\nStopped.")
    remaining = sum(1 for entry_id, text in entries if text and not (args.out / f"{entry_id}.mp3").exists())
    print(f"\nSaved {counts['saved']}, skipped {counts['skipped']}. "
          f"{remaining} entries still have no recording.")


if __name__ == "__main__":
    main()
