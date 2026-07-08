def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings *a* and *b*.

    Works for empty strings and uses a two‑row DP implementation with minimal overhead.
    """
    # Quick returns for empty inputs
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure that *a* is the longer string to minimise row size
    if len(a) < len(b):
        a, b = b, a

    # previous holds distances for the previous row (i‑1)
    previous = list(range(len(b) + 1))

    # Iterate over characters of *a*
    for i, ca in enumerate(a, 1):
        # current will hold distances for row *i*
        current = [0] * (len(b) + 1)
        current[0] = i  # distance from empty string to prefix of a

        # Compute each cell
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            insert_cost = previous[j] + 1      # insertion
            delete_cost = current[j - 1] + 1   # deletion
            replace_cost = previous[j - 1] + cost  # substitution / match
            current[j] = min(insert_cost, delete_cost, replace_cost)

        # Move to next row: previous becomes the current row for the next iteration
        if i < len(a):
            previous = current

    return previous[-1]