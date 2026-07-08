import numpy as np

def matmul(A, B):
    """
    Matrix multiplication that matches NumPy's behavior.
    Returns C where C[i,j] = sum_k(A[i,k] * B[k,j])
    """
    A = np.asarray(A)
    B = np.asarray(B)
    
    # Validate compatible shapes
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"matrices are not aligned: {A.shape} {B.shape}")
    
    return np.dot(A, B)