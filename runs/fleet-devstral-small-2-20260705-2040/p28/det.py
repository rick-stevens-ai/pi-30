def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    
    # LU decomposition with partial pivoting
    # Create augmented matrix for LU decomposition
    A = [row[:] for row in M]  # Make a copy
    
    det = 1.0
    
    for i in range(n):
        # Partial pivoting: find row with maximum element in current column
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Swap rows if needed
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            det *= -1  # Row swap changes sign of determinant
        
        # If diagonal element is zero, matrix is singular
        if abs(A[i][i]) < 1e-12:
            return 0.0
        
        # Perform elimination
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    
    # Determinant is product of diagonal elements
    for i in range(n):
        det *= A[i][i]
    
    return det
