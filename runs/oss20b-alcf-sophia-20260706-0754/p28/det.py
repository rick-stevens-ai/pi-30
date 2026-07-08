# P28 SEED: 2x2 determinant only; wrong for any larger matrix.

def determinant(M):
    """
    Compute the determinant of an NxN matrix (list of lists).
    Uses LU decomposition with partial pivoting for numerical stability.
    Mirrors numpy.linalg.det within tolerance for matrices of any size.
    """
    n = len(M)
    if n == 0:
        raise ValueError("Matrix must be non-empty")
    # Handle 1x1 explicitly
    if n == 1:
        return float(M[0][0])
    # Handle 2x2 explicitly
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # Deep copy to avoid mutating input
    A = [row[:] for row in M]
    sign = 1
    for i in range(n):
        # Partial pivoting: find row with max abs value in column i
        pivot_row = i
        max_val = abs(A[i][i])
        for r in range(i+1, n):
            val = abs(A[r][i])
            if val > max_val:
                max_val = val
                pivot_row = r
        if max_val < 1e-12:
            return 0.0
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            sign *= -1
        pivot = A[i][i]
        for r in range(i+1, n):
            factor = A[r][i] / pivot
            for c in range(i, n):
                A[r][c] -= factor * A[i][c]
    det = sign
    for i in range(n):
        det *= A[i][i]
    return float(det)
