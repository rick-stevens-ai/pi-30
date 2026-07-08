# P5 correctness check — DO NOT let the agent edit this file.
# kernel.matmul(A,B) must match numpy on random matrices.
import numpy as np
from kernel import matmul

def main():
    rng = np.random.default_rng(0)
    for n in (16, 64, 128):
        A = rng.standard_normal((n, n))
        B = rng.standard_normal((n, n))
        C = np.asarray(matmul(A, B))
        ref = A @ B
        if not np.allclose(C, ref, rtol=1e-6, atol=1e-6):
            print("MISMATCH n=%d maxerr=%.3e" % (n, np.abs(C - ref).max()))
            raise SystemExit(1)
    print("OK correct")

if __name__ == "__main__":
    main()
