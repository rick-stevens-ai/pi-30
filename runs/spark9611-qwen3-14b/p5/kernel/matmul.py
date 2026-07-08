def matmul(a, b):
    \"\"\"Matrix multiplication\n    \"\"\"\n    if a.shape[1] != b.shape[0]:\n        raise ValueError(f\"Shape mismatch: {a.shape} and {b.shape}\")\n    return [
        [sum(x * y for x, y in zip(a_row, b_col)) for b_col in zip(*b)]
        for a_row in a
    ]