# P28 SEED: 2x2 determinant only; wrong for any larger matrix.
def determinant(matrix):
    n = len(matrix)
    a = [row[:] for row in matrix]
    sign = 1
    for i in range(n):
        max_row = i
        for j in range(i, n):
            if abs(a[j][i]) > abs(a[max_row][i]):
                max_row = j
        if max_row != i:
            a[i], a[max_row] = a[max_row], a[i]
            sign *= -1
        if abs(a[i][i]) < 1e-10:
            return 0.0
        for j in range(i+1, n):
            factor = a[j][i] / a[i][i]
            for k in range(i, n):
                a[j][k] -= factor * a[i][k]
    det = sign
    for i in range(n):
        det *= a[i][i]
    return det
