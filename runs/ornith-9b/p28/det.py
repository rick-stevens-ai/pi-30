# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # WRONG fallback for n>2: just product of diagonal
    p = 1.0
    for i in range(n):
        p *= M[i][i]
    return p
