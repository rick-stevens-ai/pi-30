def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    
    # LU decomposition with partial pivoting for n>2
    # Returns det(A) = sign * product(diag(U))
    A = [row[:] for row in M]  # copy to avoid mutation
    sign = 1.0
    
    for k in range(n - 1):
        # Find pivot
        max_idx = k
        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[max_idx][k]):
                max_idx = i
        
        # Swap rows if needed
        if max_idx != k:
            A[k], A[max_idx] = A[max_idx], A[k]
            sign = -sign
        
        pivot = A[k][k]
        if abs(pivot) < 1e-15:
            return 0.0  # Singular matrix
        
        # Eliminate below
        for i in range(k + 1, n):
            factor = A[i][k] / pivot
            for j in range(k + 1, n):
                A[i][j] -= factor * A[k][j]
    
    # Determinant is sign * product of diagonal of U
    det = sign
    for i in range(n):
        det *= A[i][i]
    return det
