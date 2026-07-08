# P9 tournament scorer — DO NOT let the agent edit this file.
# Scores a candidate levenshtein.py: prints 0 if WRONG, else throughput (kops/s).
# Candidates compete to be the fastest CORRECT edit-distance implementation.
import sys
import time
import importlib.util
import random

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.levenshtein

KNOWN = [
    ("", "", 0), ("a", "", 1), ("", "abc", 3),
    ("kitten", "sitting", 3), ("flaw", "lawn", 2),
    ("gumbo", "gambol", 2), ("book", "back", 2),
    ("abcdef", "azced", 3), ("intention", "execution", 5),
    ("a"*50, "b"*50, 50),
]

def main():
    path = sys.argv[1]
    try:
        lev = load(path)
    except Exception as e:
        print("0"); return
    for a, b, d in KNOWN:
        try:
            if lev(a, b) != d:
                print("0"); return
        except Exception:
            print("0"); return
    # randomized cross-check against a trusted DP reference
    def ref(a, b):
        m, n = len(a), len(b)
        dp = list(range(n + 1))
        for i in range(1, m + 1):
            prev = dp[0]; dp[0] = i
            for j in range(1, n + 1):
                cur = dp[j]
                dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev + (a[i-1] != b[j-1]))
                prev = cur
        return dp[n]
    rng = random.Random(7)
    alpha = "abcd"
    pairs = []
    for _ in range(300):
        a = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 30)))
        b = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 30)))
        if lev(a, b) != ref(a, b):
            print("0"); return
        pairs.append((a, b))
    # timing: throughput on the validated pairs
    t0 = time.perf_counter()
    reps = 50
    for _ in range(reps):
        for a, b in pairs:
            lev(a, b)
    dt = time.perf_counter() - t0
    kops = (reps * len(pairs)) / dt / 1000.0
    print(f"{kops:.3f}")

if __name__ == "__main__":
    main()
