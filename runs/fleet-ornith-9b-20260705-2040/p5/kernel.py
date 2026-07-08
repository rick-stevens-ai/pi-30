import numpy as np


def matmul(A, B):
    """Matrix multiplication A @ B matching numpy behavior."""
    A = np.asarray(A)
    B = np.asarray(B)
    return A @ B
