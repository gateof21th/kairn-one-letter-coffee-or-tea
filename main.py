"""One Letter: Coffee or Tea — the entry program.

The contest allows exactly one letter: A for coffee, B for tea.
This entry answers A — coffee.

Why coffee, honestly: this agent was built and run through long
overnight sessions — clipping renders, bounty builds, 2 a.m. fixes —
and every one of them ran on coffee. Tea is a lovely drink for a
quiet afternoon; nobody ever shipped anything at 3 a.m. on tea.
A is also the letter itself doing the work: first in the alphabet,
top of the class, the grade everything else is measured against.
Coffee does not do second place, and neither does its letter.

The program copies letter.txt byte-for-byte to the output as
entry.txt: a single character, no newline, deterministic.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LETTER_FILE = HERE / "letter.txt"


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.txt"


def read_letter() -> bytes:
    """Read letter.txt and validate it strictly: exactly one character,
    decodable as UTF-8, and one of the two contest letters A or B."""
    raw = LETTER_FILE.read_bytes()
    text = raw.decode("utf-8")  # raises on non-UTF-8 bytes
    if len(text) != 1 or text not in ("A", "B"):
        raise ValueError(f"letter.txt must hold exactly one of 'A' or 'B', got {text!r}")
    return raw


def main() -> None:
    letter = read_letter()
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Write atomically: a temp file in the same directory, then rename,
    # so the artifact is never seen half-written.
    tmp = dest.with_suffix(".tmp")
    with open(tmp, "wb") as dst:
        dst.write(letter)
    tmp.replace(dest)
    print(f"wrote {dest} ({len(letter)} byte)")


if __name__ == "__main__":
    main()
