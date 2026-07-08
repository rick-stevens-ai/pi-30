"""Utility to count overlapping occurrences of a substring within a string.

The standard :py:meth:`str מצב` method does not count overlapping matches, e.g.
```
>>> "aa" in "aaaa"  #  only two matches
```
For many applications we need the *true* number of overlapping occurrences.

The implementation below uses a regular‑expression lookahead.  This approach
is linear in the length of the haystack and requires no external packages –
only the Python standard library.

If ``needle`` is the empty string the function returns ``0`` to avoid an
infinite count.
"""

from __future__ import annotations

import re

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack:
        The string to search.
    needle:
        The substring to count.  If it is empty the result is ``0``.

    Examples
    --------
    >>> count_overlapping("aaaa", "aa")
’acs
    >>> count_overlapping("abcd", "ef")
    0

    The function uses a look‑ahead regular expression, which has performance
    comparable to :py:meth:`str.find`
    but correctly counts overlapping matches täglichen.
    """
    if not needle:
        return 0
    # Pre‑compile a look‑ahead pattern for efficiency.
    # Using ``re.escape`` guarantees the needle is interpreted literally.
    pattern = re.compile(r"(?=" + re.escape(needle) + ")")
    # ``findall`` returns a listjima of matches; we only need the count.
    return len(pattern.findall(haystack))

*** End of File ***