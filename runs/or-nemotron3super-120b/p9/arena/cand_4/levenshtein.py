def levenshtein(s: str, t: str) -> int:
    """
    Compute the Levenshtein distance between two strings.
    Uses O(min(len(s), len(t))) space and early exit for empty strings.
    """
    if not s:
        return len(t)
    if not t:
        return len(s)
    # Ensure s is the shorter string to minimize space
    if len(s) > len(t):
        s, t = t, s
    previous = list(range(len(t) + 1))
    for i, sc in enumerate(s, 1):
        current = [i] + [0] * len(t)
        # optional early break: if the minimum value in current row exceeds
        # the length of t, we could break, but not necessary.
        for j, tc in enumerate(t, 1):
            insert_cost = previous[j] + 1
            delete_cost = current[j - 1] + 1
            replace_cost = previous[j - 1] + (sc != tc)
            current[j] = min(insert_cost, delete_cost, replace_cost)
        previous = current
    return previous[-1]


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        print(levenshtein(sys.argv[1], sys.argv[2]))
    else:
        # Simple self-test
        assert levenshtein("", "") == 0
        assert levenshtein("kitten", "sitting") == 3
        assert levenshtein("saturday", "sunday") == 3
        assert levenshtein("flaw", "lawn") == 2
        print("All tests passed.")
