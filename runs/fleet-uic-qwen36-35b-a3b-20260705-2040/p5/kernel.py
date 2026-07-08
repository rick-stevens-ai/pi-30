import numpy as np


def matmul(A, B):
    """Matrix multiplication matching NumPy exactly."""
    A = np.asarray(A)
    B = np.asarray(B)
    return (A @ B).tolist()
