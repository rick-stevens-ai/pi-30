import time
from levenshtein import levenshtein

def baseline_levenshtein(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): d[i][0] = i
    for j in range(m + 1): d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + cost)
    return d[n][m]

def benchmark():
    tests = [
        ("", ""),
        ("abc", "def"),
        ("kitten", "sitting"),
        ("intention", "execution"),
        ("a" * 10, "a" * 10),
        ("a" * 50 + "b", "a" * 50 + "c"),
        ("abc" * 20, "abd" * 20),
        ("x" * 100, "y" * 100),
    ]

    print(f"{'Test Case':<30} | {'Baseline (s)':<15} | {'Current (s)':<15}")
    print("-" * 65)
    for a, b in tests:
        t1 = time.time()
        res1 = baseline_levenshtein(a, b)
        dur1 = time.time() - t1

        t2 = time.time()
        res2 = levenshtein(a, b)
        dur2 = time.time() - t2

        assert res1 == res2, f"Mismatch: {res1} != {res2}"
        print(f"{str(a)[:15]+'...'+str(b)[:15]:<30} | {dur1:<15.6f} | {dur2:<15.6f}")

if __name__ == "__main__":
    benchmark()
