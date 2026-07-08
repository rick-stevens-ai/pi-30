def levenshtein(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein edit distance between two strings.
    Returns the minimum number of single‑character edits
    (insertions, deletions, or substitutions) required to change
    s1 into s2.

    Uses O(min(len(s1), len(s2))) space and early exit for empty strings.
    """
    # Ensure s1 is the longer (or equal) string to minimise space.
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    # If one string is empty, distance is the length of the other.
    if len(s2) == 0:
        return len(s1)

    # previous row of distances
    previous = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1, 1):
        # current row, first element is cost of deleting i chars from s1
        current = [i] + [0] * len(s2)
        for j, c2 in enumerate(s2, 1):
            insert_cost = previous[j] + 1
            delete_cost = current[j - 1] + 1
            replace_cost = previous[j - 1] + (c1 != c2)
            current[j] = min(insert_cost, delete_cost, replace_cost)
        previous = current

    return previous[-1]


if __name__ == "__main__":
    # Simple sanity checks
    assert levenshtein("", "") == 0
    assert levenshtein("", "abc") == 3
    assert levenshtein("abc", "") == 3
    assert levenshtein("abc", "abc") == 0
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("saturday", "sunday") == 3
    print("All basic tests passed.")
