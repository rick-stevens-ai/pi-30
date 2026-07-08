"""Utility to count overlapping occurrences of a substring.

The function :func:`count_overlapping` returns the number of times the
``needle`` appears in ``haystack`` allowing overlaps.  For example
``count_overlapping('aaaa', 'aa')`` returns ``3`` because the matches
start at indices ``0``, ``1`` and ``2``.

Implementation details
----------------------

* If ``needle`` is an empty string we return ``0`` – this mirrors the
  behaviour of :meth:`str.count` and prevents an infinite loop.

* For speed we use a regular expression with a *look‑ahead* assertion.
  The pattern ``(?=needle)`` finds every position where ``needle`` starts
  without consuming any characters, which naturally enables overlapping
  matches.
чной
* ``re.escape`` is used to treat the needle as a literal string (no
  special regex characters are interpreted).

The solution relies only on the Python standard library and works
efficiently even for very long strings.
"""

import re

from typing import Iterable


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of *needle* in
    *haystack*.

    Parameters
    ----------
    haystack: str
        The string to search inside.
    needle: str
        The substring to look for.

    Returns
    -------
    int
        The count of overlapping occurrences.  ``0`` is returned when
        *needle* is empty.
    """
    if not needle:
        # Per the requirements an empty needle should yield 0.
        return 0

    # ``(?=...)`` is a lookahead assertion that matches at each position
    # where the following pattern can start.  The matched string has
    # length 0, so the next call to ``finditer`` can start just one
    # character later, giving us overlapping matches.
    pattern = f"(?={re.escape(needle)})"
    return sum(1 for _ in re.finditer(pattern, haystack))


# If run directly, demonstrate functionality.
if __name__ == "__main__":  # pragma: no cover
    import sys

    if len(sys.argv) != 3:
        print("Usage: python overlap.py HAYSTACK NEEDLE")
        sys.exit(1)

    hay, new = sys.argv[1], sys.argv[2]
    print(count_overlapping(hay, new))

"""
# Usage examples
# --------------
# >>> count_overlapping('aaaa', 'aa')
# 3
# >>> count_overlapping('abababa', 'aba')
# 2
# >>> count_overlapping('abc', '')
# 0
# >>> count_overlapping('', 'a')
# 0
"""
