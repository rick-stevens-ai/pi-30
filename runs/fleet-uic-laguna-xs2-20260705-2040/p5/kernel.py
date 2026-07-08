import numpy as np


def matmul(A, B):
    """
    Matrix multiplication that matches numpy.matmul behavior.
    """
    A = np.asarray(A)
    B = np.asarray(B)
    return np.matmul(A, B)