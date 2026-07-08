import numpy as np
import numpy.linalg as LA
from det import determinant
import numpy as np

def test():
    np.random.seed(42)
    # Test random matrices
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for _ in range(2):
            A = np.random.randn(n, n)
            det_our = determinant(A.tolist())
            det_np = LA.det(A)
            if not np.isclose(det_our, det_np, rtol=1e-10, atol=1e-12):
                print(f"FAIL: n={n}")
                print(f"A:\n{A}")
                print(f"our det: {det_our}")
                print(f"numpy det: {det_np}")
                return False
    # Test singular matrices
    for n in [2, 3, 4, 5]:
        # Create a singular matrix by making two rows equal
        A = np.random.randn(n, n)
        A[1] = A[0]
        det_our = determinant(A.tolist())
        det_np = LA.det(A)
        if not np.isclose(det_our, det_np, rtol=1e-10, atol=1e-12):
            print(f"FAIL singular n={n}")
            print(f"our det: {det_our}")
            print(f"numpy det: {det_np}")
            return False
    # Test diagonal matrix
    for n in [1, 2, 3, 4, 5]:
        D = np.diag(np.random.randn(n))
        det_our = determinant(D.tolist())
        det_np = LA.det(D)
        if not np.isclose(det_our, det_np, rtol=1e-10, atol=1e-12):
            print(f"FAIL diagonal n={n}")
            return False
    print("All tests passed")
    return True

if __name__ == "__main__":
    test()