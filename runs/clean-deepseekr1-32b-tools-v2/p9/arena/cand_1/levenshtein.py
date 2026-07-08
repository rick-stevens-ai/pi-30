def levenshtein(a, b):
    if a == b:
        return 0
    len_a = len(a)
    len_b = len(b)
    
    # Handle empty string cases
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Swap to make sure we have the shorter string as a
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Initialize current and previous rows
    prev_row = list(range(len_a + 1))
    curr_row = [0] * (len_a + 1)

    for i in range(1, len_b + 1):
        curr_char = b[i-1]
        curr_row[0] = i
        for j in range(1, len_a + 1):
            prev_char = a[j-1]
            if curr_char == prev_char:
                cost = 0
            else:
                cost = 1
            # Compute the minimum of adding, removing, or replacing characters,
            # considering the current and previous positions
            curr_row[j] = min(curr_row[j-1] + 1, prev_row[j], prev_row[j-1] + cost)
        
        # Check if early exit can be applied based on current distances
        max_len_diff = abs(len_a - len_b)
        min_dist_so_far = curr_row[-1]
        if (min(i, len_a) >= len_b - (len_a - i)) or min_dist_so_far + max(0, len_b - j) >= len_a:
            break
        prev_row[:] = curr_row[:]
    
    return curr_row[len_a]