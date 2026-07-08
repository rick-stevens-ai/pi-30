# P6 verifier — DO NOT let the agent edit this file.
# reduce.parallel_sum(xs, nchunks) must return a BIT-IDENTICAL result regardless
# of how many chunks the data is partitioned into (machine-independent FP reduction).
from reduce import parallel_sum
import random

def main():
    random.seed(42)
    # mix of magnitudes to expose non-associative FP error
    xs = []
    for _ in range(100000):
        xs.append(random.choice([1e16, 1.0, -1e16, 3.14159, -2.71828, 1e-8]))
    results = {}
    for nchunks in (1, 2, 3, 4, 7, 8, 16, 100):
        results[nchunks] = parallel_sum(xs, nchunks)
    vals = set(results.values())
    if len(vals) != 1:
        print("NOT REPRODUCIBLE across chunk counts:")
        for k, v in results.items():
            print(f"  nchunks={k}: {v!r}")
        raise SystemExit(1)
    print(f"OK bit-identical: {results[1]!r}")

if __name__ == "__main__":
    main()
