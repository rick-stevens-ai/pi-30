import numpy as np

def matmul(A, B):
    """
    Performs matrix multiplication of two matrices A and B.
    Assumes A and B are lists of lists (2D arrays).

    Args:
        A (list[list[float]]): The first matrix.
        B (list[list[float]]): The second matrix.

    Returns:
        list[list[float]]: The resulting matrix C = A @ B.

    Raises:
        ValueError: If the dimensions are incompatible for multiplication.
    """
    A_np = np.array(A, dtype=np.float64)
    B_np = np.array(B, dtype=np.float64)

    if A_np.shape[1] != B_np.shape[0]:
        raise ValueError(f"Incompatible dimensions for matrix multiplication: {A_np.shape} and {B_np.shape}. Inner dimensions must match.")

    C_np = A_np @ B_np
    return C_np.tolist()