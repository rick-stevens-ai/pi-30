"""
A quick utility that counts overlapping occurrences of a substring.

Usage:
    >>> from overlap import count_overlapping
    >>> count_overlapping("aaaa", "aa")
    3

Implementation note
-------------------
We use the :py:meth:`re.findall` function with a look‑ahead assertion. This allows us to find every position where ``needle`` appears, even if those positions overlap.

The solution stays within the stdlib and runs in roughly linear time, which is plenty fast for the very long strings that often appear when working with log files in a Spark data‑pipeline setting.
"""
import re
from typing import Final

# Pre‑compiled regex pattern used as a factory.  The escape ensures special
# characters such as ``.``, ``*`` or ``\`` are treated literally.
_ESCAPE_RE: Final[re.Pattern[str]] = re.compile("(.)")

__all__ = ["count_overlapping"]


def _escape(needle: str) -> str:
    """Escape a string for use in a regular expression.

    ``re.escape`` is convenient but it produces an object that we need to
    render again.  Using a helper keeps the public function concise.
    """
    return "".join(_ESCAPE_RE.findall(re.escape(needle)))


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack:
        The string to search.
    needle:
        The substring whose overlapping occurrences we count.  An empty
        needle counts as zero, mirroring :py:meth:`str.count` and many
        other string‑matching APIs.

    Returns
    -------
    int
        The number of (possibly overlapping) matches.

    Complexity
    ----------
    The function runs in ``O(n + m)`` time, where *n* is the length of
    ``haystack`` and *m* the length of ``needle``.  Memory usage is
    ``O(m)`` for the compiled regular expression.
    """
    if not needle:
        return 0
    pattern = r"(?={})".format(_escape(needle))
    # ``re.findall`` returns a list of zero‑length matches that start where
    # ``needle`` would match, giving the desired overlapping count.
    return len(re.findall(pattern, haystack))

# If this file is executed directly we demonstrate some behaviour:
if __name__ == "__main__":  # pragma: no cover - demonstration only
    examples = [("aaaa", "aa"), ("abababa", "aba"), ("abc", "c")]
    for hay, nd in examples:
        print(f"{hay!r} contains {count_overlapping(hay, nd)} occurrences of {nd!r}")
