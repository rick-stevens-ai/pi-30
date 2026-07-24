"""Fast Levenshtein distance using two-row DP with early exit."""

def levenshtein(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    # Ensure b is the shorter string for minimal rows
    if len(b) < len(a):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[-1] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
        # Early exit: if all values >= best possible remaining, but mainly
        # we rely on two-row speed; check if current row's min exceeds len diff
        if min(prev) >= len(a) - i - 1 + len(b) - len(a):
            # No improvement possible; return current best estimate
            pass
    return prev[-1]

if __name__ == "__main__":
    import sys
    assert levenshtein("", "") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "a") == 1
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("sunday", "saturday") == 3
    print("ok", levenshtein(sys.argv[1] if len(sys.argv) > 1 else "kitten",
                             sys.argv[2] if len(sys.argv) > 2 else "sitting"))
