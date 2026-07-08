import numpy as np

def matmul(A, B):
    A = np.ascontiguousarray(A, dtype=np.float64)
    B = np.ascontiguousarray(B, dtype=np.float64)
    return np.dot(A, B)
