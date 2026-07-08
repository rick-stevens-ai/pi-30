import numpy as np


def matmul(A, B):
    """Return the matrix product of A and B.

    Parameters
    ----------
    A, B : array-like
        2-D arrays.

    Returns
    -------
    result : ndarray
        The matrix product.
    """
    # Convert inputs to numpy arrays; this is cheap for ndarray objects
    A_arr = np.asarray(A)
    B_arr = np.asarray(B)
    return np.dot(A_arr, B_arr)

