"""Count overlapping occurrences of a substring."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of OVERLAPPING occurrences of needle in haystack.

    Examples:
        count_overlapping('aaaa', 'aa')  -> 3
        count_overlapping('', '')        -> 0
        count_overlapping('abc', '')     -> 0
        count_overlapping('abc', 'd')    -> 0

    An empty needle is defined to occur zero times (avoids the infinite
    number of positions that str.find would otherwise yield).

    For non-empty needles this uses a single linear scan with
    str.find(start=...) advancing by one character each match, which is
    O(n*m) worst case but very fast in CPython thanks to the built-in
    find. For needles whose body is a single repeated character we could
    do closed-form arithmetic, but the general path below is already
    tight and correct for all inputs.
    """
    if not needle:
        return 0

    nlen = len(needle)
    # Special-case a needle made of one repeated character: occurrences
    # of a length-L run of char c in a run of length R is R - L + 1 when
    # R >= L else 0. Summing over maximal runs is O(n) and avoids any
    # per-position find overhead on degenerate inputs like 'a' * 10**7.
    first = needle[0]
    if needle == first * nlen:
        total = 0
        run = 0
        for ch in haystack:
            if ch == first:
                run += 1
            else:
                if run >= nlen:
                    total += run - nlen + 1
                run = 0
        if run >= nlen:
            total += run - nlen + 1
        return total

    # General case: repeated find, advancing start index by 1 each hit
    # so overlaps are captured. find returns -1 (or < 0) when no match.
    total = 0
    start = 0
    hlen = len(haystack)
    # Tight upper bound: last possible start is hlen - nlen.
    limit = hlen - nlen
    while start <= limit:
        idx = haystack.find(needle, start)
        if idx < 0:
            break
        total += 1
        start = idx + 1
    return total


if __name__ == "__main__":
    assert count_overlapping('aaaa', 'aa') == 3
    assert count_overlapping('', '') == 0
    assert count_overlapping('abc', '') == 0
    assert count_overlapping('abc', 'd') == 0
    assert count_overlapping('aaaa', 'a') == 4
    assert count_overlapping('ababa', 'aba') == 2
    assert count_overlapping('xxx', 'xx') == 2
    assert count_overlapping('hello', 'll') == 1
    assert count_overlapping('aaaa', 'aaa') == 2
    assert count_overlapping('a' * 10, 'a' * 3) == 8
    assert count_overlapping('abcabcabc', 'abcabc') == 2
    print("ok")
