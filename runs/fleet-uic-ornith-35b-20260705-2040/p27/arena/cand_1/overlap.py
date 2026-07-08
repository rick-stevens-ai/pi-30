"""Overlapping string search — distinct approach using finite-state automaton matching.

For non-empty needles this builds the classic KMP failure function once and then
scans the haystack exactly once, incrementing a counter every time the needle is
matched (including when matches begin one character after the previous match).

Empty-needle edge case returns 0 trivially.
"""

from __future__ import annotations


def _build_failure(needle: str) -> list[int]:
    """Classic KMP failure / prefix-function table."""
    m = len(needle)
    fail = [0] * (m + 1)
    fail[0] = -1
    i, j = 0, -1
    while i < m:
        while j >= 0 and needle[i] != needle[j]:
            j = fail[j]
        i += 1
        j += 1
        fail[i] = j
    return fail


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of (possibly overlapping) occurrences of *needle* in
    *haystack*.

    Examples::

        >>> count_overlapping("aaaa", "aa")
        3
        >>> count_overlapping("", "")
        0
        >>> count_overlapping("abc", "xyz")
        0
    """
    m = len(needle)

    # Empty needle is a degenerate input by convention (naïve counting would
    # return n+1 for length-n haystack), so we exit early.
    if m == 0:
        return 0

    # Fast path: tiny needles — let C-level find() do double duty with a
    # per-index loop; still only O(n·m) in absolute worst case but Python's
    # built-in ``find`` is implemented in C and very cache-friendly.
    if m <= 8 and m >= 1:
        count = start = 0
        while True:
            pos = haystack.find(needle, start)
            if pos == -1:
                break
            count += 1
            start = pos + 1  # slide one character — allows overlap
        return count

    # General path: full KMP automaton scan in linear time.
    fail = _build_failure(needle)
    count = 0
    j = 0  # number of matched characters so far
    for i, ch in enumerate(haystack):
        while j >= 0 and needle[j] != ch:
            j = fail[j]
        j += 1
        if j == m:
            count += 1
            j = fail[j]  # continue past the match to catch overlaps

    return count


if __name__ == "__main__":
    data: list[tuple[str, str, int]] = [
        ("aaaa", "aa", 3),
        ("ababa", "aba", 2),
        ("aaaaa", "aaa", 3),
        ("abcde", "fgh", 0),
        ("", "", 0),
        ("a", "a", 1),
        ("a" * 5, "a", 5),
    ]
    for h, n, exp in data:
        got = count_overlapping(h, n)
        status = "OK" if got == exp else "FAIL"
        print(f"{status}: haystack={h!r:<8} needle={n!r:<6} -> {got} (expected {exp})")
