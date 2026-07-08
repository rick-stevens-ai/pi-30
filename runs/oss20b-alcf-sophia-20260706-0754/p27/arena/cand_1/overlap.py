"""Utility to count overlapping occurrences of a substring.

The :func:`count_overlapping` function is a lightweight replacement for
``str.count`` that counts *overlapping* instances of a needle within a haystack.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
3
>>> count_overlapping('abc', '')
0
"""

import re
from typing import Iterable

__all__ = ["count_overlapping"]


def _validate_inputs(haystack: str, needle: str) -> None:
    """Validate the arguments.

    Parameters
    ----------
    haystack:
        The string to search within.
    needle:
        The substring to count.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(haystack, str):
        raise TypeError("haystack must be a string")
    if not isinstance(needle, str):
        raise TypeError("needle must be a string")


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    The implementation uses a regular expression with a look‑ahead assertion
    which makes it efficient even for long input strings.  ``re.finditer``
    yields zero‑length matches at each position where the ``needle`` starts.

    Special cases
    -------------
    * ``needle`` is the empty string ``""``.
        By definition we return 0, matching the behaviour required by the
        problem statement and avoiding an infinite match that the regex
        engine would otherwise produce.

    Parameters
    ----------
    haystack:
        The text to search.
    needle:
        The substring to count.

    Returns
    -------
    int
        How many times ``needle`` occurs in ``haystack``, counting
        overlapping occurrences.

    Complexity
    ----------
    • The function compiles a regular expression once per call.
    • ``re.finditer`` performs a single pass over ``haystack``.
      Therefore the time complexity is ``O(len(haystack) + len(needle))``
      and the memory usage is ``O(1)`` apart from the compiled pattern.
    """
    _validate_inputs(haystack, needle)

    # Empty needle must return 0 by definition.
    if needle == "":
        return 0

    # Escape the needle to treat it literally in the regex.
    escaped = re.escape(needle)
    # Look‑ahead ensures we find overlapping matches.
    pattern = f"(?={escaped})"
    # Compile once for slightly better performance.
    regex = re.compile(pattern)
    # Count the matches without materialising a list.
    count = 0
    for _ in regex.finditer(haystack):
        count += 1
    return count


# If run as a script, provide simple demo.
if __name__ == "__main__":
    import sys

    hay, need = sys.argv[1:3] if len(sys.argv) >= 3 else ("", "")
    print(count_overlapping(hay, need))
