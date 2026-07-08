def levenshtein(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    prev = list(range(len_b + 1))
    for i in range(1, len_a + 1):
        curr = [0] * (len_b + 1)
        curr[0] = i
        for j in range(1, len_b + 1):
            sub_cost = prev[j-1] + (0 if a[i-1] == b[j-1] else 1)
            insert_cost = prev[j] + 1
            delete_cost = curr[j-1] + 1
            curr[j] = min(sub_cost, insert_cost, delete_cost)
        prev = curr
    return prev[-1]