# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # Cofactor expansion along first row
    det = 0.0
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        cofactor = ((-1) ** j) * M[0][j] * determinant(minor)
        det += cofactor
    return det
