# P28 SEED: Using Gaussian elimination with partial pivoting for N x N determinant.
def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0
    # Create a copy to avoid mutation of the input matrix
    A = [row[:] for row in M]
    sign = 1
    
    for i in range(n):
        # Partial pivoting: find the largest element in the current column
        pivot = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[pivot][i]):
                pivot = j
        
        # Swap rows if necessary and update sign
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            sign *= -1
            
        # If the pivot element is too small, it's effectively zero (matrix is singular)
        if abs(A[i][i]) < 1e-18:
            return 0.0
            
        # Eliminate elements below the current pivot
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i + 1, n):
                A[j][k] -= factor * A[i][k]
    
    # The determinant is the product of diagonal elements multiplied by sign
    det = float(sign)
    for i in range(n):
        det *= A[i][i]
        
    return det
