# P28 SEED: Numerically stable determinant using LU decomposition
import numpy as np
def determinant(matrix):
    # Function to compute determinant using LU decomposition with partial pivoting
    
    # Make a copy of the matrix to avoid modifying the original
    A = [row[:] for row in matrix]
    n = len(A)
    det = 1.0  # Initialize determinant
    pivot_signs = 1.0

    # Base cases
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows and update determinant sign
        A[i], A[max_row] = A[max_row], A[i]
        det *= pivot_signs * (-1) ** (max_row - i)
        if i != max_row:
            pivot_signs *= -1

        # Eliminate lower entries in column i
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            
    # The product of the diagonal elements gives the determinant
    for i in range(n):
        det *= A[i][i]
    return det
