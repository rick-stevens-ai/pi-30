def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # Cofactor expansion along the first row
    det = 0.0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in M[1:]]
        det += ((-1) ** j) * M[0][j] * determinant(minor)
    return float(det)
