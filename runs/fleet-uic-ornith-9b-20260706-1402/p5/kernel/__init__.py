import numpy as np
from numba import njit, prange


@njit(parallel=True)
def _matmul_kernel(A, B):
    n = A.shape[0]
    m = B.shape[1]
    k = B.shape[0]
    C = np.zeros((n, m), dtype=np.float64)
    for i in prange(n):
        for j in range(m):
            s = 0.0
            for p in range(k):
                s += A[i, p] * B[p, j]
            C[i, j] = s
    return C


def matmul(A, B):
    """Matrix multiplication matching numpy behavior."""
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    n, k = A.shape
    assert k == B.shape[0], "incompatible dimensions"
    return _matmul_kernel(A, B)
