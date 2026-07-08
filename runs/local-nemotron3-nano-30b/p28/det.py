def determinant(M):
    """Return the determinant of a square NxN matrix M.
    The implementation uses LU decomposition via Gaussian elimination
    with partial pivoting. It computes the determinant as the product
    of the pivots, adjusted for row swaps.
    """
    n = len(M)
    if n == 0:
        raise ValueError("Empty matrix")
    # make a deep copy to avoid mutating input
    A = [list(row) for row in M]

    sign = 1.0
    det_product = 1.0

    for i in range(n):
        # Pivoting: find the row with max absolute value in column i
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if abs(A[max_row][i]) < 1e-12:
            return 0.0
        if max_row != i:
            # swap rows i and max_row
            A[i], A[max_row] = A[max_row], A[i]
            sign *= -1

        pivot = A[i][i]
        det_product *= pivot

        # Eliminate the rows below
        for j in range(i + 1, n):
            factor = A[j][i] / pivot
            # We can zero out column i; subtract factor * row i from row j
            for k in range(i + 1, n):  # columns from i+1 to end (i already zeroed)
                A[j][k] -= factor * A[i][k]
            A[j][i] = 0.0

    return det_product * sign