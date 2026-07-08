def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of needle in haystack.
    Empty needle returns 0.
    """
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1  # allow overlapping
    return count


if __name__ == "__main__":
    # Simple sanity checks
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("abcabc", "abcd") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("a", "") == 0
    assert count_overlapping("aaa", "a") == 3
    assert count_overlapping("ababababa", "aba") == 4  # positions 0,2,4,6
    assert count_overlapping("ababababa", "ab") == 4  # positions 0,2,4,6? Actually "ab" at 0,2,4,6? Let's compute: string length 9, "ab" at 0,2,4,6? indices: 0-1 ab, 2-3 ab, 4-5 ab, 6-7 ab => 4
    assert count_overlapping("mississippi", "issi") == 2  # positions 1 and 4? Actually "mississippi": issi at 1-4 and 4-7? Let's see: m i s s i s s i p p i. "issi": at index 1: i s s i? Actually index1 i,2 s,3 s,4 i => "issi". At index4: i s s i? index4 i,5 s,6 s,7 i => "issi". So two occurrences overlapping? They overlap at index4? Actually first ends at index4, second starts at index4, overlapping by one character. Overlap allowed => count 2.
    print("All tests passed")