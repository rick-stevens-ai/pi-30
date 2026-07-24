"""Matrix multiplication kernel.

C = A @ B  (matches NumPy semantics).

The algorithm is a blocked (tiled) GEMM: the matrices are partitioned
into cache-friendly blocks and each block product is computed with
NumPy's BLAS-backed ``@`` so the inner work runs at full hardware
throughput while the outer loops keep the working set cache-resident.
"""

import numpy as np

# Block size chosen for good cache behaviour on typical L2 sizes.
_BLOCK = 64


def matmul(A, B):
    """Return the matrix product ``A @ B``.

    Inputs are accepted as any array-like (lists, tuples, ndarrays) and
    are coerced to ``float64`` contiguous arrays.  The result is a
    ``float64`` ndarray matching ``np.asarray(A) @ np.asarray(B)`` to
    within floating-point rounding.
    """
    A = np.ascontiguousarray(A, dtype=np.float64)
    B = np.ascontiguousarray(B, dtype=np.float64)

    m, k = A.shape
    k2, n = B.shape
    if k != k2:
        raise ValueError(
            "incompatible shapes for matmul: %s and %s"
            % (A.shape, B.shape)
        )

    C = np.zeros((m, n), dtype=np.float64)

    # ikj loop order: the innermost loop over j reuses A[i,k] across a
    # full row of B[k,:], which is cache friendly and lets the block
    # product dispatch to an optimised BLAS dgemm.
    for ii in range(0, m, _BLOCK):
        i0, i1 = ii, ii + _BLOCK
        for kk in range(0, k, _BLOCK):
            k0, k1 = kk, kk + _BLOCK
            Ablk = A[i0:i1, k0:k1]
            for jj in range(0, n, _BLOCK):
                j0, j1 = jj, jj + _BLOCK
                C[i0:i1, j0:j1] += Ablk @ B[k0:k1, j0:j1]

    return C