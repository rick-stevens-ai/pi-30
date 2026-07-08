def levenshtein(a: str, b: str) -> int:
    """Fast Levenshtein distance using two-row DP with optimizations."""
    # Quick exits
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    
    # Ensure a is the shorter string for less memory
    if la > lb:
        a, b = b, a
        la, lb = lb, la
    
    # Common prefix
    i = 0
    while i < la and a[i] == b[i]:
        i += 1
    if i:
        a = a[i:]
        b = b[i:]
        la -= i
        lb -= i
        if la == 0:
            return lb
    
    # Common suffix
    while la > 0 and a[la - 1] == b[lb - 1]:
        la -= 1
        lb -= 1
    if la == 0:
        return lb
    a = a[:la]
    b = b[:lb]
    lb = len(b)
    
    # Two-row DP
    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)
    
    for i, ca in enumerate(a, 1):
        curr[0] = i
        p = prev[0]
        for j, cb in enumerate(b, 1):
            cur = prev[j]
            # substitution cost
            sub = p + (ca != cb)
            # deletion
            de = cur + 1
            # insertion
            ins = curr[j - 1] + 1
            p = cur
            # min of three
            if sub <= de:
                if sub <= ins:
                    curr[j] = sub
                else:
                    curr[j] = ins
            else:
                if de <= ins:
                    curr[j] = de
                else:
                    curr[j] = ins
        prev, curr = curr, prev
    
    return prev[lb]
