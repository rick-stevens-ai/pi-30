"""Count overlapping occurrences of *needle* in *haystack*.

Uses ``str.find`` (C-optimized Boyer-Moore-Horspool) with a stride of 1,
so matches share characters. Pure stdlib, O(n·m/worst-case).
"""


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:
        return 0

    n = len(needle)
    h = haystack.find(needle)
    count = 0
    while h != -1:
        count += 1
        h = haystack.find(needle, h + 1)
    return count


if __name__ == "__main__":
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("", "") == 0
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("aaa", "a") == 3
    assert count_overlapping("abcdef", "de") == 1
    assert count_overlapping("aaaaaa", "aaa") == 4
    print("ok")
