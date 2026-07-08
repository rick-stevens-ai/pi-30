import operator


def matmul(a, b):
    """Basic matrix multiplication using pure Python methods. Matched numpy's behavior for square matrices."""
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])

    # Matrix dimensions must be compatible (a_cols == b_rows)
    if a_cols != b_rows:
        raise ValueError(f'Dimming mismatch: {a_cols} columns ≠ {b_rows} rows')

    result = [[sum(operator.mul(a_row[i], b_col_i) 
              for i in range(len(a_row))))
              for a_row in a]
                  
    return result