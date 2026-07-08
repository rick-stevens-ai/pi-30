"""Utility function to count overlapping occurrences of a substring.

The function :func:`count_overlapping` returns how many times ``needle``
appears in ``haystack`` allowing overlaps.  It behaves like
``str.count`` for non‑overlapping matches but satisfies the common
scenario ``count_overlapping('aaaa', 'aa') == 3``.

The implementation uses a regular‑expression look‑ahead, which scans
``haystack`` in linear time without creating an intermediate list of
matches.  ``re`` is part of the Python standard library, so no external
dependency is required.

Typical usage:

>>> count_overlapping('hello hello', 'el')
4
>>> count_overlapping('abababa', 'aba')
3

Empty ``needle`` returns ``0`` according to the specification.
"""

from __future__ import annotations

import re
from typing import Iterable

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack:
        The string to search.
    needle:
        The substring to count.  If empty, ``0`` is returned.

    Returns
    -------
    int
        Number of overlapping matches.
    """
    if not needle:
        # Convention: empty pattern yields 0 matches.
        return 0

    # Escape the needle so that it is matched literally.
    escaped = re.escape(needle)
    # Look‑ahead pattern finds every position where ``needle`` starts.
    pattern = re.compile(f"(?={escaped})")
    return sum(1 for _ in pattern.finditer(haystack))

# ------------------------------------------------------------
# It's a small module, so we include a simple test suite when run as
# ``python -m overlap``.
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    tests: Iterable[tuple[str, str, int]] = [
        ("aaaa", "aa", 3),
        ("abcd", "ef", 0),
        ("banana", "nan", 2),
        ("", "a", 0),
        ("a", "", 0),
    ]
    ok = True
    for hay, need, exp in tests:
        res = count_overlapping(hay, need)
        if res != exp:
            print(f"FAIL: count_overlapping({hay!r}, {need!r}) => {res}, expected {exp}")
            ok = False
    if ok:
        print("All basic tests passed.")
    else:
        sys.exit(1)
