def levenshtein(a: str, b: str) -> int:
    if not a and not b:
        return 0
    len_a = len(a)
    len_b = len(b)
    # Early exit check - if either string is empty,
    if not a or not b:
        return max(len_a, len_b)
    # Swap to make sure we have the shorter in length for inner loops
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a
    prev_row = list(range(len_b + 1))
    current_row = [0] * (len_b + 1)
    for i in range(1, len_a + 1):
        if _early_row_check(prev_row, i - 1, a[i-1], b[-1]):
            return max(len_a, len_b) - (i - 1)
        current_row[0] = i
        for j in range(1, len_b + 1):
            substitution_cost = 0 if a[i-1] == b[j-1] else 1
            current_row[j] = min(
                prev_row[j] + 1,       # insertion
                current_row[j-1] + 1, # deletion
                prev_row[j-1] + substitution_cost # substitution
            )
        prev_row = current_row.copy()
    return prev_row[-1]

def _early_row_check(prev_row: list[int], i: int, a_char: str, b_last_char: str) -> bool:
    if a_char == b_last_char and len(prev_row) - (i+1) >= 0 and \ 
        sum([x for x in prev_row[:-(i+1)]]) <= 0:
        return True
    return False