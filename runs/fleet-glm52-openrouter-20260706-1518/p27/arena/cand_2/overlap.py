"""Count overlapping occurrences of needle in haystack.

Unlike str.count, occurrences may share characters. e.g. count_overlapping
('aaaa', 'aa') == 3.

Edge cases:
- empty needle -> 0 (per spec)
- needle longer than haystack -> 0

Implementation: str.find in a loop, advancing by one position each time so
that matches can overlap. This stays in C (the underlying find) and avoids
building any intermediate lists, keeping it fast on long strings.
"""

from __future__ import annotations


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    count = 0
    start = 0
    n = len(haystack)
    # Find each occurrence, then advance by just one character so the next
    # search can overlap the previous match.
    find = str.find
    while True:
        idx = find(haystack, needle, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
        if start >= n:
            break
    return count


if __name__ == "__main__":
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("aaaa", "a") == 4
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("aaaa", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    assert count_overlapping("abababa", "aba") == 3
    assert count_overlapping("xxx", "y") == 0
    assert count_overlapping("aaa", "aa") == 2
    print("all assertions passed")
