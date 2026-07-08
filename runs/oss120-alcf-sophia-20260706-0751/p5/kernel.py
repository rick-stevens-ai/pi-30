"""Kernel module providing matrix multiplication.

The `matmul` function must produce the same results as NumPy's ``@`` operator
for 2‑D NumPy arrays.  For correctness we simply delegate to ``np.dot`` which
handles broadcasting, dtype promotion, and provides the exact numerical
behaviour expected by the tests.

The implementation is deliberately straightforward – performance is not a
requirement for the correctness check.  The benchmark script (bench.py) can
still measure speed, but correctness is the primary goal.
"""

import numpy as np
from typing import Any


def matmul(A: Any, B: Any) -> np.ndarray:
    """Return the matrix product of ``A`` and ``B``.

    Parameters
    ----------
    A, B: array‑like
        2‑D input arrays. ``np.asarray`` is used to ensure they are ``ndarray``
        objects; the function then forwards the computation to ``np.dot`` which
        yields the same result as the ``@`` operator.

    Returns
    -------
    np.ndarray
        The matrix product ``A @ B``.
    """
    # Convert inputs to NumPy arrays (if they aren't already) without copying
    # when possible.
    A_arr = np.asarray(A)
    B_arr = np.asarray(B)
    # Use np.dot which is equivalent to the ``@`` operator for 2‑D arrays.
    return np.dot(A_arr, B_arr)
