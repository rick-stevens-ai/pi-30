# P28: determinant via LU decomposition with partial pivoting
# (matches numpy.linalg.det within floating-point tolerance for all n).
def determinant(M):
    n = len(M)
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]

    # Gaussian elimination with partial pivoting.
    # det(A) = (-1)^(row swaps) * product of pivots.
    A = [row[:] for row in M]  # work on a copy; don't mutate caller's matrix
    det = 1.0
    for col in range(n):
        # partial pivot: largest magnitude in this column at/below the diagonal
        pivot_row = col
        max_val = abs(A[col][col])
        for row in range(col + 1, n):
            v = abs(A[row][col])
            if v > max_val:
                max_val = v
                pivot_row = row
        if max_val == 0.0:
            return 0.0  # singular matrix
        if pivot_row != col:
            A[col], A[pivot_row] = A[pivot_row], A[col]
            det = -det
        pivot = A[col][col]
        det *= pivot
        # eliminate below the pivot
        for row in range(col + 1, n):
            factor = A[row][col] / pivot
            if factor != 0.0:
                for j in range(col, n):
                    A[row][j] -= factor * A[col][j]
    return det