# Determinant computation for an NxN matrix.
# Supports N >= 1. Uses Gaussian elimination with partial pivoting for numerical stability.
# Returns a float matching numpy.linalg.det within tolerance.

def determinant(M):
    n = len(M)
    if n == 0:
        return 1.0  # convention for empty matrix
    # Convert to float matrix copy to avoid mutating input
    A = [list(map(float, row)) for row in M]
    det = 1.0
    for i in range(n):
        # Partial pivot: find row with max absolute value in column i
        max_row = i
        max_val = abs(A[i][i])
        for r in range(i + 1, n):
            if abs(A[r][i]) > max_val:
                max_val = abs(A[r][i])
                max_row = r
        # If pivot is effectively zero, determinant is zero
        if abs(max_val) < 1e-15:
            return 0.0
        # Swap rows if needed and adjust sign
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            det *= -1.0
        pivot = A[i][i]
        det *= pivot
        # Eliminate rows below
        for r in range(i + 1, n):
            factor = A[r][i] / pivot
            # Update remaining columns
            for c in range(i + 1, n):
                A[r][c] -= factor * A[i][c]
            A[r][i] = 0.0
    return det
