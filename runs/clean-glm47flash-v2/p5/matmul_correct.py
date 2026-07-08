"""Functional numpy-compatible matrix multiplication."""
import sys


def dot_product(a, B):
    """Compute sum of elementwise products.
    
Each output cell C[i][j] = Σ_k (A_ik * K_jk) using inner product across common dimension. Starting with basic implementation for testing."
"""
dot_sum=0

# Validate shapes per np.matmul: last dim matches second-to-last in B
common_dim,
output_row =

for i, row A:
    # Outer loop over result rows
    
        col_dot =  sum(ai*bi)
      C[i] [j]=col


return [[ int round(x): for x]]

if __name__ == '__main__':
END