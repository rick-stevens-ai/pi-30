# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0
    
    # Create a copy to avoid modifying the original matrix
    A = [row[:] for row in M]
    det_sign = 1.0
    det_val = 1.0
    
    for i in range(n):
        # Find pivot (partial pivoting for stability)
        pivot = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[pivot][i]):
                pivot = j
        
        if A[pivot][i] == 0:
            # Matrix is singular or near-singular, determinant is 0
            return 0.0

        if pivot != i:
            # Swap rows
            A[i], A[pivot] = A[pivot], A[i]
            det_sign *= -1.0
            
        det_val *= A[i][i]

        # Eliminate entries below the pivot
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]

    # The determinant of an upper triangular matrix is the product of its diagonal elements.
    # We already accumulated this product into det_val.
    return det_val * det_sign
