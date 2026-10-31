# SPDX-License-Identifier: MIT
"""Import recordings exported from the browser recorder (tools/recorder).

Reads one or more zip files (or unpacked folders) with a `manifest.tsv` and
WAV files, processes each take exactly like `record_audio.py` (trim silence,
even out loudness) and saves it as `<audio>/<lang>/<id>.mp3`. Existing files
are kept unless `--overwrite` is given. Comments the reader typed in the
recorder are added to the `review` column of the matching word-list row, so
they reach the reviewers.

Usage (from the repository root):
    .venv\\Scripts\\python tools\\import_recordings.py recordings-olena-2026-11-02.zip
    .venv\\Scripts\\python tools\\import_recordings.py *.zip --overwrite
    .venv\\Scripts\\python tools\\import_recordings.py folder --no-comments
"""

import argparse
import csv
import io
import sys
import zipfile
from pathlib import Path

import soundfile as sf

from audio_processing import process, save_mp3

LANGS = ("de", "uk")


class Source:
    """A zip file or an unpacked folder exported by the recorder."""

    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if path.is_file() else None

    def read(self, name):
        if self.zip:
            return self.zip.read(name)
        return (self.path / name).read_bytes()


def read_word_lists(vocab):
    """Return {id: (file, line index)} and the files as lists of lines."""
    owners, files = {}, {}
    for path in sorted(vocab.glob("*.tsv")):
        lines = path.read_text(encoding="utf-8").split("\n")
        files[path] = lines
        head = lines[0].split("\t")
        for number, line in enumerate(lines[1:], start=1):
            if line:
                owners[line.split("\t")[head.index("id")]] = (path, number)
    return owners, files


def add_comment(files, owner, note):
    path, number = owner
    lines = files[path]
    head = lines[0].split("\t")
    cells = lines[number].split("\t")
    cells += [""] * (len(head) - len(cells))
    column = head.index("review")
    if note in cells[column]:
        return False
    cells[column] = (cells[column] + " " + note).strip()
    lines[number] = "\t".join(cells)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("sources", nargs="+", type=Path, help="zip files or folders from the recorder")
    parser.add_argument("--audio", type=Path, default=Path("audio"), help="audio root folder (default: audio)")
    parser.add_argument("--vocab", type=Path, default=Path("vocab"), help="word list folder (default: vocab)")
    parser.add_argument("--overwrite", action="store_true", help="replace existing MP3 files")
    parser.add_argument("--no-comments", action="store_true", help="don't write comments into the word lists")
    args = parser.parse_args()
    if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    owners, files = read_word_lists(args.vocab)
    counts = {"saved": 0, "kept": 0, "failed": 0, "comments": 0}
    changed = set()
    for source_path in args.sources:
        source = Source(source_path)
        manifest = source.read("manifest.tsv").decode("utf-8")
        for row in csv.DictReader(io.StringIO(manifest), delimiter="\t"):
            entry_id, lang = row["id"], row["lang"]
            label = f"{lang}/{entry_id}"
            if entry_id not in owners or lang not in LANGS:
                print(f"! {label}: not in the word lists, skipped")
                counts["failed"] += 1
                continue
            comment = (row.get("comment") or "").strip()
            if comment and not args.no_comments:
                note = f"Reader {row.get('speaker') or '?'} ({lang}): {comment}"
                if add_comment(files, owners[entry_id], note):
                    changed.add(owners[entry_id][0])
                    counts["comments"] += 1
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

    for path in sorted(changed):
        path.write_text("\n".join(files[path]), encoding="utf-8")
    print(f"\nSaved {counts['saved']}, kept {counts['kept']} existing (use --overwrite to replace), "
          f"failed {counts['failed']}, comments added {counts['comments']}.")


if __name__ == "__main__":
    main()
