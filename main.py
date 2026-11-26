#!/usr/bin/env python3
"""The Internet in One Word — make.fun entry.

Writes a single word describing the whole internet to
$MAKEFUN_OUTPUT_DIR/entry.txt.

The word is "Lurking". The internet's oldest law is 90-9-1: for every
person who posts, nine comment and ninety only watch. Billions of people
spend their days reading other people's arguments, photos and lives in
complete silence — never liking, never replying, never revealing they
were ever there. The whole internet is one vast room where almost
everyone is quietly lurking. It is funny on its own, true of the entire
internet rather than any one site, and not the first word anyone reaches
for. Pass --reason to print the pitch instead of writing the entry.
"""

import argparse
import os
import sys

WORD = "Lurking"

REASON = (
    "Ninety percent of the internet never posts, never comments, never "
    "likes — they just watch. Billions of silent readers in one loud room. "
    "The internet isn't a conversation; it's everybody lurking, all day, "
    "in every tab."
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
