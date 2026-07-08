def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0
    
    # Make a copy to avoid modifying original
    A = [row[:] for row in M]
    
    # LU decomposition with partial pivoting
    swaps = 0
    for k in range(n - 1):
        # Find pivot
        max_row = k
        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[max_row][k]):
                max_row = i
        
        if max_row != k:
            A[k], A[max_row] = A[max_row], A[k]
            swaps += 1
        
        # Check for zero pivot (singular matrix)
        if abs(A[k][k]) < 1e-15:
            return 0.0
        
        # Eliminate below
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= factor * A[k][j]
    
    # Determinant = product of diagonal * (-1)^swaps
    det = (-1) ** swaps
    for i in range(n):
        det *= A[i][i]
    
    return det