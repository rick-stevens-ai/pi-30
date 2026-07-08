# Determinant computation for an NxN matrix (list of lists).
# Uses recursive cofactor expansion which is fine for small N (≤6) as required by the tests.
def determinant(M):
    """Return the determinant of a square matrix M.

    Args:
        M (list[list[float]]): Square matrix represented as a list of rows.
    Returns:
        float: Determinant value, matching ``numpy.linalg.det`` within tolerance.
    """
    n = len(M)
    # Base cases
    if n == 0:
        return 1.0  # Determinant of empty matrix conventionally 1
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return float(M[0][0] * M[1][1] - M[0][1] * M[1][0])
    # Recursive cofactor expansion along the first row
    det = 0.0
    for col in range(n):
        # Build minor matrix excluding row 0 and column `col`
        minor = [row[:col] + row[col+1:] for row in M[1:]]
        cofactor = ((-1) ** col) * M[0][col] * determinant(minor)
        det += cofactor
    return det
