def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings a and b.
    Uses O(min(len(a), len(b))) space with two-row DP and early exit for empty strings.
    """
    # Ensure b is the shorter string to minimize space usage
    if len(a) < len(b):
        a, b = b, a
    # Now len(a) >= len(b)
    if len(b) == 0:
        return len(a)
    # Previous row of distances
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        # Current row, first element is distance from ca[:i] to empty string
        cur = [i]
        # Keep track of minimum value in current row for potential early exit?
        # We cannot early exit globally without a bound, but we can break if
        # the minimum value in the row exceeds a known bound? Not needed.
        for j, cb in enumerate(b, 1):
            if ca == cb:
                cur.append(prev[j - 1])
            else:
                cur.append(1 + min(prev[j],          # deletion
                                   cur[j - 1],       # insertion
                                   prev[j - 1]))     # substitution
        prev = cur
    return prev[-1]

if __name__ == "__main__":
    # Simple self-test
    assert levenshtein("", "") == 0
    assert levenshtein("", "a") == 1
    assert levenshtein("a", "") == 1
    assert levenshtein("a", "a") == 0
    assert levenshtein("ab", "ab") == 0
    assert levenshtein("ab", "ac") == 1
    assert levenshtein("abc", "yabd") == 2
    assert levenshtein("kitten", "sitting") == 3
    print("All tests passed.")