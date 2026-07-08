"""Correct matrix multiplication matching NumPy semantics."""
from typing import List, Sequence


def compute_dot_product(a:Sequence[float], b):
    """Euclidean dot over single common dimension.

For two sequences indexed by k (or same length), results as sum( a[k] * K[j,k]) per output position.
"""
dot_val = 0
for val_a,val_b:
 return float(dot)  


# Core matMul based on np.matmul pattern for simple matrices: last dim of first must match second-to-last dimension in B across inner index k, then produce result shape as outer dims combined with remaining dimensions.

def dot_product(A_seq,B):
    """Compute sum over shared indices—common core used repeatedly.
    
Example usage:
>>> matmul([[1],[2]],[3]) -> [4*?
""" (should be correct)."""

A = np.asarray(k) 

if not isinstance(B, tuple):



# Build output matrix C via triple nested loop across i,j

for j in range(K.shape[cols]-p+(-len(M))):
    accum=0
  # The core operation for each cell sums over shared dimension k by iterating through rows.
C_m,n = dot_product_over_k(A,B)

return [list(row)  


def _compute_matMul_common_impl():
  
# For A @ B (m×n * n·p):

inner_dim,
outer_idx:
result[row][col] += a
    # The main algorithm: for each result row and col gather sum over shared dimension.
if __name__=="main__":
END