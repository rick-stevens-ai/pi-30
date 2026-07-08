# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)

    # Check if it is a square matrix (N x N)
    for row in M:
        if len(row) != n:
            raise ValueError("Matrix must be square.")

    A = [[float(M[i][j]) for j in range(n)] for i in range(n)]
    det_sign = 1.0
    TOLERANCE = 1e-9

    for k in range(n):
        # Find pivot (partial pivoting for numerical stability)
        pivot_row = k
        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[pivot_row][k]):
                pivot_row = i

        # Swap rows if necessary
        if pivot_row != k:
            A[k], A[pivot_row] = A[pivot_row], A[k]
            det_sign *= -1.0

        # Check for singularity
        if abs(A[k][k]) < TOLERANCE:
            return 0.0

        # Eliminate entries below the pivot
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]

    # Determinant is the product of diagonal elements times the sign change
    det_val = det_sign
    for i in range(n):
        det_val *= A[i][i]
    return det_val
