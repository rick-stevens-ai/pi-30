"""Count overlapping occurrences of *needle* in *haystack* using KMP.

>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('ababab', 'ab')
3
>>> count_overlapping('hello', '')
0
>>> count_overlapping('', 'x')
0
>>> count_overlapping('abc', 'abc')
1
>>> count_overlapping('aaaa', 'a')
4
>>> count_overlapping('abab', 'abab')
1
>>> count_overlapping('aaa', 'aa')
2
>>> count_overlapping('mississippi', 'issi')
2
"""


def _build_failure(needle: str) -> list[int]:
    """Return the KMP failure (partial-match) table for *needle*.

    failure[j] = length of the longest proper prefix of needle[:j+1]
    that is also a suffix of needle[:j+1].
    """
    m = len(needle)
    failure = [0] * m
    k = 0
    for j in range(1, m):
        while k > 0 and needle[k] != needle[j]:
            k = failure[k - 1]
        if needle[k] == needle[j]:
            k += 1
        failure[j] = k
    return failure


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of *needle* in *haystack*.

    An empty needle always returns 0 (there is nothing to match).
    Runs in O(n + m) time and O(m) extra space via KMP.
    """
    if not needle:
        return 0

    n, m = len(haystack), len(needle)
    if m > n:
        return 0

    failure = _build_failure(needle)
    count = 0
    q = 0  # characters of needle matched so far

    for i in range(n):
        while q > 0 and needle[q] != haystack[i]:
            q = failure[q - 1]
        if needle[q] == haystack[i]:
            q += 1
        if q == m:
            count += 1
            q = failure[q - 1]  # resume for overlapping matches

    return count


if __name__ == "__main__":
    # Quick smoke tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("aaaa", "a") == 4
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("", "x") == 0
    assert count_overlapping("ababab", "ab") == 3
    assert count_overlapping("mississippi", "issi") == 2
    assert count_overlapping("abc", "abc") == 1
    print("All smoke tests passed.")
