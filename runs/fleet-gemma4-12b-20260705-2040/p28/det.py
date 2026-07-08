def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0
    if n == 1:
        return float(M[0][0])
    
    # Create a copy to avoid modifying the input matrix
    A = [row[:] for row in M]
    det = 1.0
    
    for i in range(n):
        # Partial pivoting: find the largest element in the current column
        max_val = -1.0
        pivot_row = -1
        for k in range(i, n):
            if abs(A[k][i]) > max_val:
                max_val = abs(A[k][i])
                pivot_row = k
        
        if max_val == 0.0:
            return 0.0
        
        # Swap rows if the current row is not the pivot row
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            det *= -1.0
            
        det *= A[i][i]
        
        # Eliminate elements below the pivot
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i + 1, n):
                A[k][j] -= factor * A[i][j]
                
    return float(det)
