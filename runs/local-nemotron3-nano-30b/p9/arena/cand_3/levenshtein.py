def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein edit distance between strings `a` and `b`.

    The implementation uses a two‑row DP table (O(min(len(a), len(b))) space)
    and runs in O(len(a) * len(b)) time. It correctly handles empty inputs
    and can exit early when the strings are identical or one of them is empty.

    Args:
        a: First string.
        b: Second string.

    Returns:
        The edit distance as an integer.
    """
    # Early exits for trivial cases
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure the shorter string drives the inner loop to minimise work
    if len(a) > len(b):
        a, b = b, a

    previous_row = list(range(len(a) + 1))

    for j in range(1, len(b) + 1):
        current_row = [j] + [0] * len(a)
        ch_b = b[j - 1]

        for i, ch_a in enumerate(a, start=1):
            cost = 0 if ch_a == ch_b else 1
            deletion = previous_row[i] + 1
            insertion = current_row[i - 1] + 1
            substitution = previous_row[i - 1] + cost

            current_row[i] = min(deletion, insertion, substitution)

        # Early exit if we somehow fill a row with all zeros (both strings equal)
        # This can only happen when the remaining suffix is identical.
        if not any(current_row):
            return 0

        previous_row = current_row

    return previous_row[-1]