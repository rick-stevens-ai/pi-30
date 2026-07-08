# Determinant calculation for an NxN matrix.
# Implements LU decomposition with partial pivoting to compute the determinant.
# Returns a float. Matches numpy.linalg.det within typical tolerance for n>2.

def determinant(M):
    """Return the determinant of a square matrix M (list of lists).

    The algorithm performs Gaussian elimination with partial pivoting, tracking
    row swaps to adjust the sign of the determinant. It works for any size N ≥ 1
    and returns a float.
    """
    n = len(M)
    if n == 0:
        raise ValueError("Empty matrix")
    # Ensure matrix is square
    for row in M:
        if len(row) != n:
            raise ValueError("Matrix must be square")

    # Base cases for speed and exactness
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return float(M[0][0] * M[1][1] - M[0][1] * M[1][0])

    # Make a deep copy to avoid mutating the input
    A = [list(map(float, row)) for row in M]
    det_sign = 1.0
    for k in range(n):
        # Partial pivot: find the row with the largest absolute value in column k
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        if abs(A[max_row][k]) < 1e-15:
            # Singular matrix
            return 0.0
        if max_row != k:
            # Swap rows
            A[k], A[max_row] = A[max_row], A[k]
            det_sign *= -1.0
        pivot = A[k][k]
        # Eliminate rows below
        for i in range(k + 1, n):
            factor = A[i][k] / pivot
            # Update the rest of the row
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
    # Product of diagonal elements gives the determinant of U
    det = det_sign
    for i in range(n):
        det *= A[i][i]
    return det

