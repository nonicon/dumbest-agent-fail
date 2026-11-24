"""Dumbest Agent Fail — make.fun entry.

Writes one line about the dumbest thing my agent did today to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line is validated against the kit gate (1-200 chars, single line,
not only whitespace, valid UTF-8) before writing, and read back
afterwards to confirm the file holds exactly the validated line.
"""

import os
import sys

LINE = (
    "My agent looped for forty minutes summarizing a PDF that turned out "
    "to be a photo of a sandwich, then offered me the executive summary."
)

# The sealed gate from the kit's RULES.txt: /output/entry.txt must be
# UTF-8 text of 1 to 200 characters, not only whitespace, one line.
MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Enforce the gate before anything is written."""
    if not text:
        raise ValueError("entry must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS}-char gate"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> int:
    try:
        validate_entry(LINE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Round-trip: read back what the grader will see and confirm it is
    # byte-for-byte the validated line, so a truncated write can never
    # slip through as a valid-looking entry.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        print(f"error: wrote {written!r}, expected {LINE!r}", file=sys.stderr)
        return 1
    print(f"entry written to {path}: {written!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
