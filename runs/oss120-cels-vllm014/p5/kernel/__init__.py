# Kernel module for matrix multiplication
# Implements a simple matmul that matches NumPy's @ operator.
# The function accepts two 2‑D NumPy arrays (or array‑like) and returns
# their matrix product as a NumPy ndarray.

import numpy as np


def matmul(A, B):
    """Return the matrix product of A and B.

    Parameters
    ----------
    A, B : array_like
        Input matrices. They are converted to ``np.ndarray`` with ``dtype``
        ``float64`` (matching the default used in the tests).

    Returns
    -------
    np.ndarray
        The result of ``A @ B``.
    """
    # Ensure inputs are NumPy arrays of compatible shape.
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    if A.ndim != 2 or B.ndim != 2:
        raise ValueError("matmul only supports 2‑D matrices")
    if A.shape[1] != B.shape[0]:
        raise ValueError(
            f"inner dimensions must match: {A.shape[1]} (A columns) != {B.shape[0]} (B rows)"
        )
    # Use NumPy's dot for correctness and simplicity.
    return np.dot(A, B)
