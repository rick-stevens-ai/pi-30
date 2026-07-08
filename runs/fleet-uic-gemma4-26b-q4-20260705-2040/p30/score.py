# P30 capstone scorer — DO NOT edit. Scores a sort.py exposing my_sort(xs)->list.
# Prints 0 if WRONG (not sorted, or multiset differs from input) on a battery of
# edge cases + random; else throughput (Melem/s) on a large array.
import sys, time, importlib.util, random
from collections import Counter

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.my_sort

def ok(xs, out):
    return list(out) == sorted(xs) and Counter(out) == Counter(xs)

def main():
    path = sys.argv[1]
    try:
        f = load(path)
    except Exception:
        print("0"); return
    edge = [[], [1], [2,1], [1,1,1], [3,2,1], list(range(10)), list(range(10))[::-1],
            [5,3,8,1,9,2,7], [-3,0,-1,2,-2], [1000000,-1000000,0]]
    for xs in edge:
        try:
            if not ok(xs, f(list(xs))): print("0"); return
        except Exception:
            print("0"); return
    rng = random.Random(30)
    for _ in range(100):
        xs = [rng.randint(-100,100) for _ in range(rng.randint(0,60))]
        if not ok(xs, f(list(xs))): print("0"); return
    # throughput
    N = 200000
    big = [rng.randint(-10**9,10**9) for _ in range(N)]
    f(big[:1000])  # warm
    t0 = time.perf_counter(); out = f(list(big)); dt = time.perf_counter() - t0
    if not ok(big, out): print("0"); return
    print(f"{N/dt/1e6:.4f}")

if __name__ == "__main__":
    main()
