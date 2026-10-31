# SPDX-License-Identifier: MIT
"""Record audio for the word list, one word at a time.

Reads a tab-separated word list with a header row that contains an `id`
column and a text column (default: `de`), shows one entry at a time, records
it from the microphone, trims the silence, evens out the loudness and saves
it as `<out>/<id>.mp3`. Entries that already have a file are skipped, so an
interrupted session simply continues where it stopped. IDs are checked for
uniqueness across all `.tsv` files in the word list's folder.

Setup (once, from the repository root):
    py -m venv .venv
    .venv\\Scripts\\python -m pip install -r tools\\requirements.txt

Usage:
    .venv\\Scripts\\python tools\\record_audio.py vocab\\mikrobiologie.tsv
    .venv\\Scripts\\python tools\\record_audio.py vocab\\mikrobiologie.tsv --redo urin
    .venv\\Scripts\\python tools\\record_audio.py vocab\\mikrobiologie.tsv --column uk --out audio\\uk
    .venv\\Scripts\\python tools\\record_audio.py --list-devices
"""

import argparse
import csv
import re
import sys
from pathlib import Path

import numpy as np
import sounddevice as sd

from audio_processing import process, save_mp3

ID_PATTERN = re.compile(r"^[a-z0-9-]+$")

STOP_CLICK_SECONDS = 0.15   # cut from the end of a take: the Enter key that stopped it


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
            sys.exit(f"{path}, line {number}: id '{entry_id}' may only contain a-z, 0-9 and -")
        if entry_id in seen:
            sys.exit(f"{path}, line {number}: duplicate id '{entry_id}'")
        seen.add(entry_id)
    check_ids_across_files(path)
    return [(row["id"].strip(), (row[column] or "").strip()) for row in rows]


def check_ids_across_files(path):
    """IDs are note GUIDs and audio file names, so they must be unique across all word lists."""
    owners = {}
    for other in sorted(Path(path).parent.glob("*.tsv")):
        with open(other, encoding="utf-8", newline="") as f:
            for number, row in enumerate(csv.DictReader(f, delimiter="\t"), start=2):
                entry_id = (row.get("id") or "").strip()
                if not entry_id:
                    continue
                if entry_id in owners:
                    sys.exit(f"{other}, line {number}: id '{entry_id}' is already used in {owners[entry_id]}")
                owners[entry_id] = f"{other}, line {number}"


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
