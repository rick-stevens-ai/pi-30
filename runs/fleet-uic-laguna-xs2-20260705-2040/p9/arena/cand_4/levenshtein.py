"""Levenshtein edit distance - optimized two-row DP implementation."""


def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein edit distance between two strings.

    Uses two-row dynamic programming with early exits for optimal performance.
    Space complexity: O(min(len(a), len(b)))
    Time complexity: O(len(a) * len(b))

    Args:
        a: First string
        b: Second string

    Returns:
        Minimum number of single-character edits (insertions, deletions, substitutions)
        needed to transform a into b.
    """
    # Early exit: identical strings
    if a == b:
        return 0

    # Early exit: empty strings
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure a is the longer string to minimize inner loop iterations
    if len(a) < len(b):
        a, b = b, a

    # Two-row DP: prev_row[j] = distance(a[0:i-1], b[0:j])
    # Initialize with costs for transforming empty string to b prefixes
    prev_row = list(range(len(b) + 1))

    for i in range(1, len(a) + 1):
        # First element: cost of deleting all characters from a[0:i]
        current_row = [i]

        for j in range(1, len(b) + 1):
            substitution_cost = 0 if a[i - 1] == b[j - 1] else 1
            current_row.append(
                min(
                    current_row[j - 1] + 1,      # insertion
                    prev_row[j] + 1,              # deletion
                    prev_row[j - 1] + substitution_cost  # substitution
                )
            )

        prev_row = current_row

    return prev_row[-1]