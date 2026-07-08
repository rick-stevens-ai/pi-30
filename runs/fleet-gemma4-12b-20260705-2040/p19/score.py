# P19 tournament: fastest CORRECT nth-Fibonacci that must handle huge n exactly
# (Python bigint) AND be fast at n=200000. Scorer prints 0 if wrong, else a
# throughput-ish score. Naive recursion or slow loops lose to fast-doubling.
import sys, time, importlib.util

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.fib

def ref(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def main():
    path = sys.argv[1]
    try:
        f = load(path)
    except Exception:
        print("0"); return
    for n in (0, 1, 2, 3, 10, 50, 100, 1000):
        try:
            if f(n) != ref(n):
                print("0"); return
        except Exception:
            print("0"); return
    # big-n correctness + timing
    N = 200000
    t0 = time.perf_counter()
    try:
        val = f(N)
    except Exception:
        print("0"); return
    dt = time.perf_counter() - t0
    if val != ref(N):
        print("0"); return
    print(f"{1.0/dt:.4f}")  # higher = faster

if __name__ == "__main__":
    main()
