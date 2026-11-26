#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One word for the whole internet.

This is an entry for make.fun's "The Internet in One Word" bounty. The
answer it gives is a single word: Doomscrolling.

Why that word? Because the defining act of being online today is not
looking something up or reading something through — it is thumbing an
endless feed of alarming headlines long after you meant to stop. Every
platform converged on the same design: a bottomless stream that never
runs out of worse news. Doomscrolling is the habit the internet itself
created; no newspaper or television channel ever offered an infinite
feed of dread. It fits the whole internet rather than one app, and it is
not the obvious first word that springs to mind.

Running this script writes the word, followed by a newline, to
``entry.txt`` inside the directory named by MAKEFUN_OUTPUT_DIR, and
makes the file world-readable (mode 0644) so the grader can read it no
matter what the sandbox umask is. Pass ``--reason`` to print the pitch
instead of writing the entry.
"""

import argparse
import os
import sys

WORD = "Doomscrolling"

PITCH = (
    "The internet stopped being a library and became a feed. Every app "
    "now serves an endless stream built to keep a thumb moving, and the "
    "thing we all end up doing inside that stream is doomscrolling: one "
    "more alarming headline, one more thread, until it is 2 a.m. and "
    "nothing was learned. No older medium ever offered an infinite "
    "supply of bad news, so the word belongs to the internet alone — and "
    "to all of it, not to any single site."
)

MAX_LENGTH = 30
ENTRY_FILENAME = "entry.txt"
OUTPUT_MODE = 0o644


def _reject_if_blank(word):
    """Return an error message when the word is empty or all whitespace."""
    if not word or not word.strip():
        return "entry must not be empty or only whitespace"
    return None


def _reject_if_split(word):
    """Return an error message when the word contains any whitespace."""
    if any(ch.isspace() for ch in word):
        return "entry must be a single word with no whitespace inside"
    return None


def _reject_if_too_long(word):
    """Return an error message when the word exceeds the length limit."""
    if len(word) > MAX_LENGTH:
        return f"entry must be at most {MAX_LENGTH} characters long"
    return None


def _reject_if_not_plain_text(word):
    """Return an error message unless the word is plain printable ASCII."""
    if not word.isascii() or not word.isprintable():
        return "entry must be plain printable ASCII so it reads as one clean word"
    return None


# The checks run in this order so the most basic failure is reported first.
WORD_RULES = (
    _reject_if_blank,
    _reject_if_split,
    _reject_if_too_long,
    _reject_if_not_plain_text,
)


def validate_word(word):
    """Raise ValueError if the word would fail the competition's gate."""
    for rule in WORD_RULES:
        problem = rule(word)
        if problem is not None:
            raise ValueError(problem)


def build_parser():
    """Build the command-line parser for this entry."""
    parser = argparse.ArgumentParser(
        description="Write one word describing the whole internet."
    )
    parser.add_argument(
        "--reason",
        action="store_true",
        help="print why Doomscrolling describes the whole internet",
    )
    return parser


def resolve_output_dir():
    """Return the output directory from the environment, or None."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR")


def save_entry(word, directory):
    """Write ``word`` plus a newline to entry.txt and make it readable.

    Returns the path written. The file is deliberately set to mode 0644:
    an earlier entry of ours was rejected because the grader could not
    read a 0600 output file under the sandbox umask.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, ENTRY_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(word + "\n")
    os.chmod(path, OUTPUT_MODE)
    return path


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.reason:
        print(f"{WORD}: {PITCH}")
        return 0
    validate_word(WORD)
    output_dir = resolve_output_dir()
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    path = save_entry(WORD, output_dir)
    print(f"wrote {WORD!r} to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
