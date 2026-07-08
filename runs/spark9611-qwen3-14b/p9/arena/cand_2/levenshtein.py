def levenshtein(a, b):
    len_diff = abs(len(a) - len(b))
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(a) + 1))
    for i in range(1, len(b) + 1):
        curr = [0] * (len(a) + 1)
        curr[0] = prev[0] + 1
        for j in range(1, len(a) + 1):
            cost = 0 if a[j-1] == b[i-1] else 1
            curr[j] = min(curr[j-1] + 1, prev[j] + 1, prev[j-1] + cost)
        if curr[-1] == len_diff:
            return curr[-1]
        prev = curr
    return prev[-1]