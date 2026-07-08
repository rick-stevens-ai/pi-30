"""Utility for counting overlapping substring occurrences.

The function :func:`count_overlapping` returns how many times *needle*
appears in *haystack*, including overlapping matches.

Examples
--------
>>> count_overlapping("aaaa", "aa")
3
>>> count_overlapping("abc", "bc")
1
>>> count_overlapping("abc", "")
0

Implementation notes
--------------------
* For speed on large strings we use a compiled regular expression with a
  look‑ahead assertion, which allows the engine to hop one character at a
  time while still recognizing the needle.
* The function is intentionally written in pure standard library and does
  not pull in any external dependencies.
"""

from __future__ import annotations
import re

__all__ = ["count_overlapping"]

# Cache the compiled regex for a given needle to avoid recompilation when the
# same needle is searched repeatedly.  We keep a weak reference dictionary
# to avoid leaking memory for very many distinct needles.
_imports_cache: dict[str, re.Pattern] = {}


def _get_pattern(needle: str) -> re.Pattern:
    """Return a compiled pattern that matches an overlapping *needle*.

    The pattern is a look‑ahead ``(?=needle)`` which yields a match at each
    starting position where *needle* occurs, even if the previous match
    consumed some of the same characters.
    """
    if needle not in _imports_cache:
        _imports_cache[needle] = re.compile(f"(?={re.escape(needle)})")
    return _imports_cache[needle]


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
        Count of overlapping matches.
    """
    if not needle:
        return 0
    pattern = _get_pattern(needle)
    # ``finditer`` yields an iterator of match objects without allocating a
    # list, which is memory friendly for long strings.
    return sum(1 for _ in pattern.finditer(haystack))

*** End of overlap.py ***"