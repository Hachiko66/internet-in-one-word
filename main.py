#!/usr/bin/env python3
"""The Internet in One Word — make.fun entry.

Writes a single word describing the whole internet to
$MAKEFUN_OUTPUT_DIR/entry.txt.

The word is "Captcha": the one ritual every human on the internet shares —
proving to a machine that you are not a machine. Funny on its own, true of
the whole internet rather than one site, and not the first word anyone
reaches for.
"""

import os
import sys

WORD = "Captcha"

# The sealed gate: entry.txt must be UTF-8 text of 1 to 30 characters,
# not only white space. Refuse to write anything that would fail it.
MAX_CHARS = 30


def validate(word: str) -> None:
    if not word or word.strip() == "":
        raise ValueError("word must not be empty or only whitespace")
    if " " in word or "\t" in word or "\n" in word:
        raise ValueError("entry must be a single word, no whitespace inside")
    if len(word) > MAX_CHARS:
        raise ValueError(f"word must be at most {MAX_CHARS} characters")


def main() -> int:
    validate(WORD)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(WORD + "\n")
    # The grader requires the output file to be world-readable (mode 0644)
    # regardless of the sandbox umask — a past entry was rejected for a
    # 0600 output.
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
