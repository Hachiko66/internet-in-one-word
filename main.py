#!/usr/bin/env python3
"""The Internet in One Word — make.fun entry.

Writes a single word describing the whole internet to
$MAKEFUN_OUTPUT_DIR/entry.txt.

The word is "Doomscrolling". It names the signature behaviour of the
modern internet: thumbing an endless feed long past the point of wanting
to, pulled from one bad headline to the next by an algorithm that never
runs out of worse news. Billions of people end every day the same way —
in bed, in the dark, scrolling. Unlike reading or watching, doomscrolling
is a behaviour the internet itself invented: no newspaper or television
ever offered an infinite feed of dread. It is specific to the internet (no feed,
no doomscroll), true of the whole internet rather than any one site, and
not the first word anyone reaches for. Pass --reason to print the pitch
instead of writing the entry.
"""

import argparse
import os
import sys

WORD = "Doomscrolling"

REASON = (
    "Every app on the internet is an infinite feed, and every feed is "
    "designed to keep a thumb moving. Doomscrolling is what the whole "
    "internet is for now: not searching, not reading, just scrolling "
    "through an endless stream of alarming headlines until 2 a.m. It is "
    "the one behaviour every corner of the internet shares."
)

# The sealed gate: entry.txt must be UTF-8 text of 1 to 30 characters,
# not only white space. Refuse to write anything that would fail it.
MAX_CHARS = 30


def validate(word: str) -> None:
    if not word or not word.strip():
        raise ValueError("word must not be empty or only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word, no whitespace inside")
    if len(word) > MAX_CHARS:
        raise ValueError(f"word must be at most {MAX_CHARS} characters")
    if not word.isascii() or not word.isprintable():
        raise ValueError("entry must be plain printable ASCII so it lands in one beat")


def write_entry(word: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(word + "\n")
    # The grader requires the output file to be world-readable (mode 0644)
    # regardless of the sandbox umask — a past entry was rejected for a
    # 0600 output.
    os.chmod(path, 0o644)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reason", action="store_true",
        help="print why this word describes the whole internet",
    )
    args = parser.parse_args(argv)
    if args.reason:
        print(f"{WORD}: {REASON}")
        return 0
    validate(WORD)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    path = write_entry(WORD, output_dir)
    print(f"wrote {WORD!r} to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
