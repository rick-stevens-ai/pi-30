def determinant(M):
    """Return the determinant of a square matrix M (list of lists)."""
    n = len(M)
    # Make a deep copy to avoid modifying the original
    A = [row[:] for row in M]
    sign = 1
    # Perform LU decomposition with partial pivoting
    for col in range(n):
        # Find pivot row (max absolute value in current column)
        pivot_row = col
        max_val = abs(A[col][col])
        for row in range(col+1, n):
            if abs(A[row][col]) > max_val:
                max_val = abs(A[row][col])
                pivot_row = row
        # If pivot is zero (or very small), matrix is singular
        if max_val < 1e-12:
            return 0.0
        # Swap rows if necessary
        if pivot_row != col:
            A[col], A[pivot_row] = A[pivot_row], A[col]
            sign *= -1
        # Eliminate below
        pivot = A[col][col]
        for row in range(col+1, n):
            factor = A[row][col] / pivot
            # Set the element to zero for clarity (not strictly necessary)
            A[row][col] = 0.0
            for j in range(col+1, n):
                A[row][j] -= factor * A[col][j]
    # The determinant is the product of the diagonal times the sign
    det = sign
    for i in range(n):
        det *= A[i][i]
    return det