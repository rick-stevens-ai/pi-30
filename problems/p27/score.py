# P27 tournament: fastest CORRECT substring search count (count overlapping
# occurrences of needle in haystack). Scorer prints 0 if wrong else throughput.
# Candidates compete; naive O(nm) loses to str.count / KMP / etc. NOTE overlapping
# count required (e.g. count "aa" in "aaaa" == 3), which str.count does NOT do,
# so candidates must be cleverer than the obvious.
import sys, time, importlib.util, random

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.count_overlapping

def ref(h, n):
    if not n: return 0
    c = 0; i = 0
    while True:
        j = h.find(n, i)
        if j < 0: break
        c += 1; i = j + 1
    return c

def main():
    path = sys.argv[1]
    try:
        f = load(path)
    except Exception:
        print("0"); return
    fixed = [("aaaa","aa",3),("","a",0),("abc","",0),("abababab","abab",3),
             ("mississippi","issi",2),("aaa","b",0),("xyz","xyz",1)]
    for h,n,d in fixed:
        try:
            if f(h,n) != d: print("0"); return
        except Exception:
            print("0"); return
    rng = random.Random(27)
    big = "".join(rng.choice("ab") for _ in range(20000))
    cases = [(big, "".join(rng.choice("ab") for _ in range(rng.randint(1,5)))) for _ in range(200)]
    for h,n in cases:
        if f(h,n) != ref(h,n): print("0"); return
    t0 = time.perf_counter()
    for _ in range(20):
        for h,n in cases: f(h,n)
    dt = time.perf_counter() - t0
    print(f"{1.0/dt:.4f}")

if __name__ == "__main__":
    main()
