#!/usr/bin/env python3
"""It Blinked First: a two-sentence horror story.

The program writes one fixed story to /output/entry.txt for the make.fun
Two-Sentence Horror bounty (u-suroto-two-sentence-horror-acea9253).

Deterministic by design: the same 153 bytes on every run. No input, no
network, no randomness, no clock, no environment reads -- the story below
is the whole entry, and this program only carries it to the output file
and verifies, by reading it back, that the file holds exactly that text.
"""

import hashlib
import os

# The story, exactly as the judge will read it: two sentences, 153 chars.
STORY = (
    "The mirror in the hallway has shown my reflection a half-second late "
    "since we moved in, and I stopped noticing months ago. "
    "This morning it blinked first."
)

# Pinned digest of STORY, so a run can prove the output is byte-identical.
EXPECTED_SHA256 = "e2cdb71849c7d2c3dae836490014e90b744770ae4ec05914578006b09aba4912"
EXPECTED_BYTES = 153


def main() -> None:
    text = STORY
    if not 1 <= len(text) <= 400:
        raise ValueError(f"story is {len(text)} characters, must be 1-400")
    if not text.strip():
        raise ValueError("story must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("story must fit on one line")
    terminators = sum(text.count(mark) for mark in ".?!")
    if terminators != 2:
        raise ValueError(f"story has {terminators} sentence terminators, must be exactly two sentences")
    if len(text.encode("utf-8")) != EXPECTED_BYTES:
        raise ValueError(f"story is {len(text.encode('utf-8'))} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != EXPECTED_SHA256:
        raise ValueError("story digest does not match EXPECTED_SHA256")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError("read-back mismatch: /output/entry.txt differs from STORY")
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise ValueError("read-back digest does not match EXPECTED_SHA256")


if __name__ == "__main__":
    main()
