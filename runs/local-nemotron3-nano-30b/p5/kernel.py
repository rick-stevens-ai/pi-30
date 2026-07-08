import numpy as np

def matmul(a, b):
    """
    Matrix multiplication that matches numpy's @ operator exactly.
    
    This implementation uses NumPy's internal matmul function to ensure
    numerical results are identical to a @ b for all input shapes.
    """
    return a @ b