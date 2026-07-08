# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # Cofactor expansion along first row for n > 2
    det = 0.0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in M[1:]]
        sign = (-1) ** col
        det += sign * M[0][col] * determinant(minor)
    return det
