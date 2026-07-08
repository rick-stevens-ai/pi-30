def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein distance between two strings a and b
    using a space-optimized two-row dynamic programming approach.
    """
    len_a = len(a)
    len_b = len(b)

    # Optimization: Ensure a is the shorter string for minimal space complexity O(min(len_a, len_b))
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Handle edge cases where one string is empty
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Initialize the previous row (representing distances for an empty prefix of a)
    # Size is len_a + 1
    previous_row = list(range(len_a + 1))

    for j in range(1, len_b + 1):
        current_row = [j]  # Distance from empty string a to b[:j] is j (insertions)
        for i in range(1, len_a + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            
            # Calculate minimum of:
            # 1. Deletion: previous_row[i] + 1 (deletion from a)
            # 2. Insertion: current_row[-1] + 1 (insertion into a, which corresponds to distance for a[:i] vs b[:j-1])
            # 3. Substitution: previous_row[i - 1] + cost (substitution/match)
            
            deletion = previous_row[i] + 1
            insertion = current_row[-1] + 1
            substitution = previous_row[i - 1] + cost
            
            current_row.append(min(deletion, insertion, substitution))
        
        previous_row = current_row

    return previous_row[len_a]

if __name__ == '__main__':
    # Test cases
    print(f"levenshtein('kitten', 'sitting'): {levenshtein('kitten', 'sitting')}") # Expected: 3
    print(f"levenshtein('flaw', 'lawn'): {levenshtein('flaw', 'lawn')}")       # Expected: 2
    print(f"levenshtein('', 'abc'): {levenshtein('', 'abc')}")                 # Expected: 3
    print(f"levenshtein('abc', ''): {levenshtein('abc', '')}")                 # Expected: 3
    print(f"levenshtein('', ''): {levenshtein('', '')}")                     # Expected: 0
    print(f"levenshtein('abc', 'abc'): {levenshtein('abc', 'abc')}")           # Expected: 0
    print(f"levenshtein('a', 'b'): {levenshtein('a', 'b')}")                   # Expected: 1
    print(f"levenshtein('abc', 'axc'): {levenshtein('abc', 'axc')}")           # Expected: 1
