# SPDX-License-Identifier: MIT
"""Import recordings and checks exported from the browser recorder (tools/recorder).

Reads one or more zip files (or unpacked folders) with a `manifest.tsv` and
WAV files, and for each entry:

- processes the take exactly like `record_audio.py` (trim silence, even out
  loudness) and saves it as `<audio>/<lang>/<id>.mp3`; existing files are kept
  unless `--overwrite` is given;
- if the reader confirmed the entry ("all correct"), removes the review items
  they were shown from the `review` column;
- if the reader wrote a comment, adds it to the `review` column.

Takes and checks whose text no longer matches the word list (because the entry
was changed after recording) are skipped with a warning. At the end the
script lists draft rows whose `review` cell is now empty, so their status can
be set to `ok`.

Usage (from the repository root):
    .venv\\Scripts\\python tools\\import_recordings.py recordings-olena-2026-11-02.zip
    .venv\\Scripts\\python tools\\import_recordings.py *.zip --overwrite
"""

import argparse
import csv
import io
import re
import sys
import zipfile
from pathlib import Path

import soundfile as sf

from audio_processing import process, save_mp3

LANGS = ("de", "uk")
# Review items: the review cell is split before each prefix. Must match tools/recorder/index.html.
ITEM_SPLIT = re.compile(r"\s+(?=(?:UK|DE|EN|Build|Reader [^:()]{1,60} \((?:uk|de)\)):)")
ITEM_SEPARATOR = " ¦ "   # how the recorder joins the items it showed


def review_items(text):
    return [item.strip() for item in ITEM_SPLIT.split(text or "") if item.strip()]


class Source:
    """A zip file or an unpacked folder exported by the recorder."""

    def __init__(self, path):
        self.zip = zipfile.ZipFile(path) if path.is_file() else None
        self.path = path

    def read(self, name):
        return self.zip.read(name) if self.zip else (self.path / name).read_bytes()


class WordLists:
    """All word lists, edited in place line by line so their format is kept."""

    def __init__(self, folder):
        self.lines, self.where, self.changed = {}, {}, set()
        for path in sorted(folder.glob("*.tsv")):
            lines = path.read_text(encoding="utf-8").split("\n")
            self.lines[path] = lines
            for number, line in enumerate(lines[1:], start=1):
                if line:
                    self.where[line.split("\t")[0]] = (path, number)

    def get(self, entry_id):
        path, number = self.where[entry_id]
        head = self.lines[path][0].split("\t")
        cells = self.lines[path][number].split("\t")
        return dict(zip(head, cells + [""] * (len(head) - len(cells))))

    def set_review(self, entry_id, review):
        path, number = self.where[entry_id]
        head = self.lines[path][0].split("\t")
        cells = self.lines[path][number].split("\t")
        cells += [""] * (len(head) - len(cells))
        cells[head.index("review")] = review
        self.lines[path][number] = "\t".join(cells)
        self.changed.add(path)

    def save(self):
        for path in sorted(self.changed):
            path.write_text("\n".join(self.lines[path]), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("sources", nargs="+", type=Path, help="zip files or folders from the recorder")
    parser.add_argument("--audio", type=Path, default=Path("audio"), help="audio root folder (default: audio)")
    parser.add_argument("--vocab", type=Path, default=Path("vocab"), help="word list folder (default: vocab)")
    parser.add_argument("--overwrite", action="store_true", help="replace existing MP3 files")
    parser.add_argument("--no-review", action="store_true", help="import audio only; leave the word lists unchanged")
    args = parser.parse_args()
    if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    lists = WordLists(args.vocab)
    counts = dict(saved=0, kept=0, failed=0, stale=0, confirmed=0, comments=0)
    touched = set()
    for source_path in args.sources:
        source = Source(source_path)
        manifest = source.read("manifest.tsv").decode("utf-8")
        for row in csv.DictReader(io.StringIO(manifest), delimiter="\t"):
            entry_id, lang = row["id"], row["lang"]
            label = f"{lang}/{entry_id}"
            if entry_id not in lists.where or lang not in LANGS:
                print(f"! {label}: not in the word lists, skipped")
                counts["failed"] += 1
                continue
            entry = lists.get(entry_id)
            if row["text"] != entry[lang]:
                print(f"! {label}: the text changed since it was recorded or checked "
                      f"('{row['text']}' → '{entry[lang]}'), skipped")
                counts["stale"] += 1
                continue

            if not args.no_review:
                items = review_items(entry["review"])
                if row.get("verdict") == "ok":
                    shown = set(filter(None, (row.get("items") or "").split(ITEM_SEPARATOR)))
                    remaining = [item for item in items if item not in shown]
                    if remaining != items:
                        lists.set_review(entry_id, " ".join(remaining))
                        counts["confirmed"] += 1
                        touched.add(entry_id)
                comment = (row.get("comment") or "").strip()
                if comment:
                    note = f"Reader {row.get('speaker') or '?'} ({lang}): {comment}"
                    if note not in items:
                        lists.set_review(entry_id, " ".join(review_items(lists.get(entry_id)["review"]) + [note]))
                        counts["comments"] += 1
                        touched.add(entry_id)

            if not row.get("file"):
                continue
            out = args.audio / lang / f"{entry_id}.mp3"
            if out.exists() and not args.overwrite:
                counts["kept"] += 1
                continue
            raw, samplerate = sf.read(io.BytesIO(source.read(row["file"])), dtype="float32", always_2d=True)
            audio, warnings = process(raw.mean(axis=1), samplerate)
            for warning in warnings:
                print(f"! {label}: {warning}")
            if audio is None:
                counts["failed"] += 1
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            save_mp3(audio, samplerate, out)
            counts["saved"] += 1
            print(f"✓ {out}")

    lists.save()
    print(f"\nAudio: saved {counts['saved']}, kept {counts['kept']} existing (use --overwrite to replace), "
          f"failed {counts['failed']}, skipped as outdated {counts['stale']}.")
    print(f"Review: {counts['confirmed']} entries confirmed, {counts['comments']} comments added.")
    ready = sorted(entry_id for entry_id in touched
                   if not lists.get(entry_id)["review"] and lists.get(entry_id)["status"] == "draft")
    if ready:
        print(f"No open review items any more (status can be set to ok): {', '.join(ready)}")


if __name__ == "__main__":
    main()
