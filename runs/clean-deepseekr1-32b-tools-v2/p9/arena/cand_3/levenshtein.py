def levenshtein(a: str, b: str) -> int:
    len_a = len(a)
    len_b = len(b)
    
    if len_a == 0 or len_b == 0:
        return max(len_a, len_b)

    # Initialize two rows for iterative DP
    prev_row = list(range(len_b + 1))
    curr_row = [0]*(len_b + 1)

    for i in range(1, len_a + 1):
        # Set the current row's first element
        curr_row[0] = i
        a_char = a[i-1]
        
        for j in range(1, len_b + 1):
            b_char = b[j-1]
            if a_char == b_char:
                curr_row[j] = prev_row[j-1]
            else:
                curr_row[j] = 1 + min(curr_row[j-1],
                                      prev_row[j-1],
                                      prev_row[j])
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, [0]*(len_b + 1)

    return prev_row[len_b]
