import numpy as np

def matmul(A, B):
    """
    Performs matrix multiplication A @ B.
    Assumes A and B are compatible matrices (e.g., NumPy arrays or lists of lists).
    For simplicity and matching NumPy behavior in a general context, 
    we use numpy's implementation here. If this kernel is meant to be pure Python/C-like 
    without relying on external libraries like numpy for the core logic, 
    the implementation needs to be rewritten based on specific constraints.
    """
    try:
        return np.matmul(A, B)
    except TypeError:
        # Fallback if inputs are not NumPy arrays but standard Python lists/tuples
        # This is a basic implementation for demonstration; real kernel might require optimization.
        if len(A[0]) != len(B):
            raise ValueError("Matrices dimensions mismatch for multiplication.")
        
        rows_a = len(A)
        cols_a = len(A[0])
        rows_b = len(B)
        cols_b = len(B[0])

        if cols_a != rows_b:
             raise ValueError("Inner dimensions must match.")

        C = [[0] * cols_b for _ in range(rows_a)]
        for i in range(rows_a):
            for j in range(cols_b):
                sum_val = 0
                for k in range(cols_a):
                    sum_val += A[i][k] * B[k][j]
                C[i][j] = sum_val
        return C

if __name__ == '__main__':
    # Simple test case
    A_test = [[1, 2], [3, 4]]
    B_test = [[5, 6], [7, 8]]
    C_result = matmul(A_test, B_test)
    print("Test result:", C_result)

