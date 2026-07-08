# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    """Compute the determinant of an NxN matrix.

    The implementation uses Gaussian elimination with partial pivoting to
    match :func:`numpy.linalg.det` within floating‑point tolerance.
    Parameters
    ----------
    M : list[list[float]]
        Square matrix as a list of lists.
    Returns
    -------
    float
        Determinant of ``M``.
    """
    n = len(M)
    if n == 0:
        # Empty matrix has no determinant; return 1 to match np.linalg.det([]) which errors.
        return 0.0
    if n == 1:
        return float(M[0][0])
    # Make a shallow copy because we will modify the matrix
    A = [row[:] for row in M]
    sign = 1
    eps = 1e-12
    for i in range(n):
        # Partial pivot: find row with max abs value in column i
        pivot = i
        maxabs = abs(A[i][i])
        for j in range(i + 1, n):
            if abs(A[j][i]) > maxabs:
                maxabs = abs(A[j][i])
                pivot = j
        if maxabs < eps:  # singular matrix
            return 0.0
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            sign *= -1
        # Eliminate below
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i + 1, n):
                A[j][k] -= factor * A[i][k]
    det = sign
    for i in range(n):
        det *= A[i][i]
    return det
