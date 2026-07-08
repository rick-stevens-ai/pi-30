import reduce
import random

def test():
    for seed in [1, 42, 12345, 999]:
        random.seed(seed)
        xs = [random.choice([1e16, 1.0, -1e16, 3.14159, -2.71828, 1e-8]) for _ in range(10000)]
        results = {}
        for nchunks in [1, 2, 3, 4, 5, 7, 8, 16, 32, 100, 1000]:
            results[nchunks] = reduce.parallel_sum(xs, nchunks)
        vals = set(results.values())
        if len(vals) != 1:
            print(f"Seed {seed}: NOT reproducible")
            for k, v in results.items():
                print(f"  nchunks={k}: {v!r}")
            return False
        else:
            print(f"Seed {seed}: OK {list(vals)[0]}")
    return True

if __name__ == "__main__":
    test()
