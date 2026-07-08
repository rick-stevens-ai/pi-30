def determinant(M):
    """Compute determinant of NxN matrix using LU decomposition with partial pivoting."""
    n = len(M)
    if n == 0:
        return 1.0
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return float(M[0][0]*M[1][1] - M[0][1]*M[1][0])
    
    # Make a copy to avoid modifying input
    A = [row[:] for row in M]
    
    # LU decomposition with partial pivoting
    # Track row permutations for sign
    sign = 1
    
    for k in range(n - 1):
        # Find pivot
        max_row = k
        max_val = abs(A[k][k])
        for i in range(k + 1, n):
            if abs(A[i][k]) > max_val:
                max_val = abs(A[i][k])
                max_row = i
        
        # If pivot is zero, matrix is singular
        if max_val == 0:
            return 0.0
        
        # Swap rows if needed
        if max_row != k:
            A[k], A[max_row] = A[max_row], A[k]
            sign *= -1
        
        # Eliminate below pivot
        pivot = A[k][k]
        for i in range(k + 1, n):
            factor = A[i][k] / pivot
            A[i][k] = factor  # Store L factor
            for j in range(k + 1, n):
                A[i][j] -= factor * A[k][j]
    
    # Determinant is product of diagonal elements of U times sign
    det = sign
    for i in range(n):
        det *= A[i][i]
    
    return float(det)
