import numpy as np
import numpy.linalg as LA
from det import determinant
import numpy as np

def test():
    # Test random matrices of various sizes
    np.random.seed(42)
    for n in [1, 2, 3, 4, 5, 6]:
        for _ in range(3):
            A = np.random.randn(n, n)
            det_our = determinant(A.tolist())
            det_np = LA.det(A)
            if not np.isclose(det_our, det_np, rtol=1e-10, atol=1e-12):
                print(f"FAIL: n={n}")
                print(f"A:\n{A}")
                print(f"our det: {det_our}")
                print(f"numpy det: {det_np}")
                return False
    print("All tests passed")
    return True

if __name__ == "__main__":
    test()