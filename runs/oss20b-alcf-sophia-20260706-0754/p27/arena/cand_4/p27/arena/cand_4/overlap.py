"""Utility to count overlapping substring occurrences.

The :func:`count_overlapping` function implements a fast
implementation based on the regular‑expression engine which is
efficient for typical ASCII text. It adheres to the following
specification:

* ``count_overlapping('aaaa', 'aa')`` → ``3`` (overlap allowed).
* ``count_overlapping('abc', '')`` → ``0`` (empty needle).
* Only the standard library is used.

The implementation uses a *look‑ahead* pattern ``(?=needle)`` which
matches a position before an occurrence of ``needle`` without
consuming characters.  The built‑in :func:`re.findall` returns a list
of all such positions; its length is the desired count.

This approach is considerably faster than a manual loop for long
strings because the regex engine performs the search in C and
handles back‑tracking efficiently.
"""

from __future__ import annotations

import re
from typing import Final

# Regular expression that will be compiled lazily on first use.
# The pattern is dynamically created based on the needle, so we
# cannot cache it globally.  The function itself is lightweight.

__all__: Final = ["count_overlapping"]

def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack:
        The string to search.
    needle:
        The substring to look for.  An empty ``needle`` always
        yields ``0``.
    """
    if not needle:
        return 0
    # Escape any regex metacharacters in the needle.
    escaped = re.escape(needle)
    # Build a look‑ahead pattern that finds every position where the
    # needle starts.  ``(?=...)`` does not consume characters.
    pattern = f"(?={escaped})"
    # Find all non‑overlapping matches of the look‑ahead pattern.
    matches = re.findall(pattern, haystack)
    return len(matches)

# If this module is run directly, perform a quick sanity check.
if __name__ == "__main__":  # pragma: no cover
    tests = [
        ("aaaa", "aa", 3),
        ("abc", "", 0),
        ("abababa", "aba", 2),
        ("", "a", 0),
        ("aaaaa", "a", 5),
        ("abcdef", "def", 1),
        ("abcdef", "xyz", 0),
    ]
    for h, n, expected in tests:
        result = count_overlapping(h, n)
        assert result == expected, f"{h!r},{n!r} → {result} != {expected}"
    print("All tests passed.")
