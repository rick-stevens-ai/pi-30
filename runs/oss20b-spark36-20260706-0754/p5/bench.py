# P5 benchmark — DO NOT let the agent edit this file.
# Prints GFLOP/s for kernel.matmul on a 512x512 GEMM. Used as the loop signal.
import sys
import time
import numpy as np
from kernel import matmul

def main():
    report = "--report" in sys.argv
    n = 256
    rng = np.random.default_rng(1)
    A = rng.standard_normal((n, n))
    B = rng.standard_normal((n, n))
    matmul(A, B)  # warmup (numba JIT etc.)
    best = float("inf")
    for _ in range(3):
        t0 = time.perf_counter()
        matmul(A, B)
        dt = time.perf_counter() - t0
        best = min(best, dt)
    gflops = 2.0 * n**3 / best / 1e9
    if report:
        print(f"{gflops:.4f}")
    else:
        print(f"matmul {n}x{n}: {best*1e3:.2f} ms  {gflops:.3f} GFLOP/s")

if __name__ == "__main__":
    main()
