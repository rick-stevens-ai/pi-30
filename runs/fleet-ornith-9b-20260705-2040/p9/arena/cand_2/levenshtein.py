def levenshtein(a: str, b: str) -> int:
    """Compute edit distance between a and b using two-row DP."""
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return max(n, m)

    # Iterate over shorter string for cache locality
    if n > m:
        a, b = b, a
        n, m = m, n

    ao = [ord(c) for c in a]
    bo = [ord(c) for c in b]

    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        curr[0] = i
        ai = ao[i - 1]

        for j in range(m):
            if ai == bo[j]:
                curr[j + 1] = prev[j]
            else:
                v = prev[j]
                if curr[j] < v:
                    v = curr[j]
                if prev[j + 1] < v:
                    v = prev[j + 1]
                curr[j + 1] = v + 1

        prev, curr = curr, prev

    return prev[m]
