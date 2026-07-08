# P28 oracle: matrix determinant via LU/expansion, checked against numpy on
# random matrices. Seed only works for 2x2. Tolerance generous (FP).
from det import determinant
import numpy as np

def main():
    rng = np.random.default_rng(28)
    worst = 0.0
    for n in (1, 2, 3, 4, 5, 6):
        for _ in range(50):
            M = rng.standard_normal((n, n)).tolist()
            got = determinant([row[:] for row in M])
            exp = float(np.linalg.det(np.array(M)))
            denom = max(1.0, abs(exp))
            err = abs(got - exp) / denom
            worst = max(worst, err)
            if err > 1e-6:
                print(f"MISMATCH n={n} got={got:.6f} exp={exp:.6f} err={err:.2e}")
                raise SystemExit(1)
    # singular + identity sanity
    assert abs(determinant([[1,2],[2,4]])) < 1e-9
    assert abs(determinant([[1,0,0],[0,1,0],[0,0,1]]) - 1.0) < 1e-9
    print(f"OK P28 worst={worst:.2e}")

if __name__ == "__main__":
    main()
