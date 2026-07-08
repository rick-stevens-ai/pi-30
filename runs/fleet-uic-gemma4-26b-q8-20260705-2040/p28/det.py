# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0 # Conventionally det of empty matrix is 1
    if n == 1:
        return float(M[0][0])
    
    # Work on a copy to avoid modifying the input
    A = [row[:] for row in M]
    det = 1.0
    
    for i in range(n):
        # Pivot selection (partial pivoting)
        pivot_idx = i
        max_val = abs(A[i][i])
        for k in range(i + 1, n):
            if abs(A[k][i]) > max_val:
                max_val = abs(A[k][i])
                pivot_idx = k
        
        # If pivot is zero (or very close to it), determinant is 0
        if max_val < 1e-18: # Using a small epsilon for stability
            return 0.0
            
        # Swap rows if necessary
        if pivot_idx != i:
            A[i], A[pivot_idx] = A[pivot_idx], A[i]
            det *= -1.0
            
        det *= A[i][i]
        
        # Elimination
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i + 1, n):
                A[k][j] -= factor * A[i][j]
                
    return det
