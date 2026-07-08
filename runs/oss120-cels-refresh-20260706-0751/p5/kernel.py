import numpy as np

def matmul(A, B):
    """Matrix multiplication matching NumPy's ``@`` operator.

    Parameters
    ----------
    A, B : array-like
        Two-dimensional arrays with compatible shapes.

    Returns
    -------
    np.ndarray
        The matrix product ``A @ B``.
    """
    # Convert inputs to NumPy arrays (if they aren't already)
    A_arr = np.asarray(A)
    B_arr = np.asarray(B)
    # Use NumPy's dot which follows the same broadcasting rules as ``@``
    return np.dot(A_arr, B_arr)
