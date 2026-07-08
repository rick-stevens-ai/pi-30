import numpy as np

def matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Return the matrix product of A and B.
    Delegates to :func:`numpy.matmul` for correct numpy semantics.
    """
    return np.matmul(A, B)
