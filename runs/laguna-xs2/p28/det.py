# P28: Determinant via LU decomposition with partial pivoting.
def determinant(M):
    import copy
    n = len(M)
    if n == 0:
        return 1.0
    # Work on a copy
    A = copy.deepcopy(M)
    det = 1.0
    for k in range(n):
        # Find pivot
        max_idx = k
        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[max_idx][k]):
                max_idx = i
        # Swap rows if needed
        if max_idx != k:
            A[k], A[max_idx] = A[max_idx], A[k]
            det *= -1
        # Check for singular
        if abs(A[k][k]) < 1e-15:
            return 0.0
        # Eliminate below
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
    # Product of diagonal (U matrix)
    for i in range(n):
        det *= A[i][i]
    return det
