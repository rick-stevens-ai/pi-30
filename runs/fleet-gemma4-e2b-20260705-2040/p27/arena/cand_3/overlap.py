def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search within.
        needle: The substring to count.

    Returns:
        The number of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    count = 0
    start_index = 0
    n_len = len(needle)

    while True:
        # Find the next occurrence starting from start_index
        found_index = haystack.find(needle, start_index)

        if found_index == -1:
            break

        count += 1
        # For overlapping matches, we advance the search position by only 1
        # to allow for an overlap at the next possible position.
        start_index = found_index + 1

    return count

if __name__ == '__main__':
    # Test case: 'aa' in 'aaaa' should be 3 (at indices 0, 1, 2)
    h1, n1 = 'aaaa', 'aa'
    r1 = count_overlapping(h1, n1)
    print(f"'{n1}' in '{h1}': {r1} (Expected: 3)")

    # Test case: No overlap
    h2, n2 = 'abcde', 'a'
    r2 = count_overlapping(h2, n2)
    print(f"'{n2}' in '{h2}': {r2} (Expected: 1)")

    # Test case: Non-overlapping
    h3, n3 = 'ababab', 'aba'
    # Matches at index 0 ('aba'), index 2 ('aba'), index 4 ('aba'). Total 3. Wait, this is overlapping.
    # Index 0: aba (haystack[0:3])
    # Index 1: bab (no)
    # Index 2: aba (haystack[2:5]) -> Overlaps with previous one at index 2.
    # Index 3: bab (no)
    # Index 4: aba (haystack[4:7] - out of bounds if length is 6, indices 0-5)
    # 'ababab' (length 6)
    # i=0: 'aba'. Next search at 1.
    # i=1: 'bab'. No. Search from 2.
    # i=2: 'aba'. Found. Count=2. Next search at 3.
    # i=3: 'bab'. No. Search from 4.
    # i=4: 'ab' (not enough). Stop. Wait, let's re-trace for 'ababab', needle='aba'. Length 3.
    # h[0:3] = aba. Count=1. start_index=1.
    # find('aba', 1) -> finds at index 2 ('aba' starting at index 2). Count=2. start_index=3.
    # find('aba', 3) -> finds at index 4 (haystack[4:7] is 'ab'). No, it searches from index 3. hay[3]='b', hay[4]='a', hay[5]='b'. Not found.
    # Let's re-run the logic mentally for 'ababab', needle='aba':
    # start_index = 0. find('aba', 0) -> returns 0. count=1. start_index=1.
    # start_index = 1. find('aba', 1) -> returns 2. count=2. start_index=3.
    # start_index = 3. find('aba', 3) -> returns -1 (haystack[3:] is 'bab'). Break.
    # Expected: 2.

    h4, n4 = 'ababab', 'aba'
    r4 = count_overlapping(h4, n4)
    print(f"'{n4}' in '{h4}': {r4} (Expected: 2)")


    # Test case: Empty needle requirement
    h5, n5 = 'test', ''
    r5 = count_overlapping(h5, n5)
    print(f"Empty needle test: {r5} (Expected: 0)")

    # Test case: Needle longer than haystack
    h6, n6 = 'short', 'longer'
    r6 = count_overlapping(h6, n6)
    print(f"Longer needle test: {r6} (Expected: 0)")