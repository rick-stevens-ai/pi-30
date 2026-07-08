# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return float(M[0][0]*M[1][1] - M[0][1]*M[1][0])

    # Use Gaussian elimination to compute determinant
    A = [row[:] for row in M]
    det = 1.0
    swaps = 0
    
    for i in range(n):
        pivot_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        
        if abs(A[pivot_row][i]) < 1e-15:
            return 0.0
        
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            swaps += 1
        
        det *= A[i][i]
        
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i + 1, n):
                A[j][k] -= factor * A[i][k]
    
    return det * ((-1)**swaps)
