def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein distance between two strings a and b.
    Uses a two-row dynamic programming approach for O(min(m, n)) space complexity.
    """
    if a == b:
        return 0
    
    # Ensure 'a' is the shorter string to minimize space complexity
    if len(a) > len(b):
        a, b = b, a
    
    m, n = len(a), len(b)
    
    if m == 0:
        return n
    
    # current_row[j] will hold the distance between a[:i] and b[:j]
    # We only need the previous row to compute the current row.
    previous_row = list(range(m + 1))
    current_row = [0] * (m + 1)
    
    for j in range(1, n + 1):
        current_row[0] = j
        for i in range(1, m + 1):
            # Cost of substitution
            cost = 0 if a[i - 1] == b[j - 1] else 1
            
            # min(deletion, insertion, substitution)
            current_row[i] = min(
                current_row[i - 1] + 1,      # insertion
                previous_row[i] + 1,          # deletion
                previous_row[i - 1] + cost    # substitution
            )
        # Move current to previous for next iteration
        previous_row[:] = current_row
        
    return previous_row[m]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(levenshtein(sys.argv[1], sys.argv[2]))
