def determinant(M):
    n = len(M)
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    det = 0.0
    for c in range(n):
        # minor matrix removing row 0 and column c
        minor = [row[:c] + row[c+1:] for row in M[1:]]
        sign = -1 if c % 2 else 1
        det += sign * M[0][c] * determinant(minor)
    return det
