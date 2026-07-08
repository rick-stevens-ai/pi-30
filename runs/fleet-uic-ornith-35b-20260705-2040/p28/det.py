# P28 seed fix: determinant via cofactor expansion along the first row.
def _minor(M, skip_row, skip_col):
    """Return the submatrix with skip_row and skip_col removed."""
    return [M[r] for r in range(len(M)) if r != skip_row]

def determinant(M):
    n = len(M)
    if n == 1:
        return float(M[0][0])
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    # Cofactor expansion along the first row
    result = 0.0
    for j in range(n):
        sub = [row[:j] + row[j+1:] for i, row in enumerate(M) if i > 0]
        coef = M[0][j] * (-1) ** j * determinant(sub)
        result += coef
    return float(result)
