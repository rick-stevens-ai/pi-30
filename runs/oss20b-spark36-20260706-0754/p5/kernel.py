import numpy as np

def matmul(A, B):
    """Return the matrix product of A and B.

    The result is computed using NumPy's @ operator which guarantees
    identical numerical behaviour to ``np.dot`` for 2‑D arrays.

    Parameters
    ----------
    A : array_like
        Left operand, shape (m, k).
    B : array_like
        Right operand, shape (k, n).

    Returns
    -------
    ndarray
        Result of the matrix multiplication with dtype promoted according to NumPy rules.
    """
    A_arr = np.asarray(A)
    B_arr = np.asarray(B)

    if A_arr.ndim != 2 or B_arr.ndim != 2:
        raise ValueError("matmul requires two dimensional arrays")
    if A_arr.shape[1] != B_arr.shape[0]:
        raise ValueError(
            f"shapes {A_arr.shape} and {B_arr.shape} not aligned: {A_arr.shape[1]} (dim 1) vs {B_arr.shape[0]} (dim 0)"
        )

    # Use NumPy's @ operator for correctness.
    return A_arr @ B_arr
