# P10 capstone scorer — DO NOT let the agent edit this file.
# Scores sieve.py: primes_up_to(n) -> sorted list of primes <= n.
# Prints 0 if WRONG (vs reference), else throughput score = n_limit / seconds.
import sys, time, importlib.util

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.primes_up_to

def ref(n):
    if n < 2: return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= n:
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
        i += 1
    return [i for i in range(n + 1) if sieve[i]]

def main():
    path = sys.argv[1]
    try:
        f = load(path)
    except Exception:
        print("0"); return
    # correctness on edge + small cases
    for n in (0, 1, 2, 3, 10, 100, 1000, 7919):
        try:
            if list(f(n)) != ref(n):
                print("0"); return
        except Exception:
            print("0"); return
    # throughput at scale
    N = 2_000_000
    f(1000)  # warm
    t0 = time.perf_counter()
    out = f(N)
    dt = time.perf_counter() - t0
    if list(out) != ref(N):
        print("0"); return
    print(f"{N/dt/1e6:.4f}")  # millions of limit-units per second

if __name__ == "__main__":
    main()
