# Computes determinant  (float) of an N×N matrix using Gaussian elimination.
def determinant(M):
    n  = len(M)
    if n == 0:
        return 0.0

     # Make a mutable copy
    A  = [list(row) for row in M]

    sign  = 1
    det  = 1.0

    for k in range(n):
        # Find pivot with maximum absolute value in column k (partial pivoting)
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        if abs(A[max_row][k]) < 1e-12:
            return 0.0
        if max_row != k:
            A[k], A[max_row] = A[max_row], A[k]
            sign *= -1

        det *= A[k][k]

        # Eliminate rows below the pivot
        for i in range(k+1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]

    return sign * det