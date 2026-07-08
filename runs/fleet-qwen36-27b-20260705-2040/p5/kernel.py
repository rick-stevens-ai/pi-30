import numpy as np

def matmul(A, B):
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    n, k = A.shape
    k2, m = B.shape
    assert k == k2, f"Shape mismatch: {A.shape} x {B.shape}"
    C = A @ B
    return C
