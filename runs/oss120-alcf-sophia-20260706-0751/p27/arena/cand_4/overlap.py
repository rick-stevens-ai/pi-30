import re

__all__ = ["count_overlapping"]

def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abc', '')
    0
    >>> count_overlapping('', 'a')
    0

    The implementation uses a look‑ahead regular expression, which runs in
    linear time on the size of ``haystack`` (the underlying regex engine is
    written in C). An empty ``needle`` is defined to yield ``0`` occurrences,
    matching the typical expectations for this utility.
    """
    if not needle:
        return 0
    # ``(?=needle)`` is a zero‑width positive look‑ahead that matches at each
    # position where ``needle`` starts, thus counting overlapping matches.
    pattern = re.compile(r"(?={})".format(re.escape(needle)))
    return sum(1 for _ in pattern.finditer(haystack))
