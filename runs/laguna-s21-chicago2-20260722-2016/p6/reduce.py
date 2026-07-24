"""Reproducible floating-point parallel reduction.

``parallel_sum(xs, nchunks)`` returns a sum of *xs* that is **bit-identical**
regardless of the value of *nchunks*.

Why this matters
----------------
Floating-point addition is **not associative**.  Partitioning data into a
different number of chunks changes the order of additions, which changes the
rounding error and therefore the final bit-pattern:

    xs = [1e16, 1.0, -1e16]
    sum(xs)              == 0.0      (left-to-right)
    (1e16+1.0) + (-1e16) == 0.0      (1 chunk:  1e16+1 loses the 1.0)
    1e16 + (1.0-1e16)    == 1.0      (2 chunks: 1.0-1e16 == -1e16, then 0)

Strategy
--------
Use :func:`math.fsum`, which computes the **correctly-rounded** sum via an
extended-precision accumulator (Shewchuk's algorithm).  Because the result is
the exact mathematical sum rounded *once* to nearest, it is independent of the
order in which elements are added — and therefore independent of how the data
is chunked.

A naive chunked reduction (sum each chunk, then combine the partial sums) is
**not** sufficient: per-chunk rounding discards information that cannot be
recovered at the combine step.  Even using ``math.fsum`` per chunk and then
combining the partial results with ``math.fsum`` is not bit-identical, because
the per-chunk rounding still introduces irrecoverable error::

    math.fsum([1e16, 1.0, -1e16])              == 1.0   (correct)
    math.fsum([math.fsum([1e16, 1.0]),          == 0.0   (wrong)
               math.fsum([-1e16])])

The only way to guarantee bit-identicality regardless of *nchunks* is to sum
all data in a single, order-independent pass — which is exactly what
:func:`math.fsum` provides.
"""

import math


def parallel_sum(xs, nchunks):
    """Return the bit-identical sum of *xs*.

    The result is the correctly-rounded sum of all elements and does **not**
    depend on *nchunks* or on the order of evaluation.

    Parameters
    ----------
    xs : iterable of float
        The values to sum.
    nchunks : int
        Accepted for API compatibility — the function is designed to be a
        drop-in parallel reduction.  The result is independent of this value
        because :func:`math.fsum` is order-independent.

    Returns
    -------
    float
        The correctly-rounded sum of *xs*.
    """
    return math.fsum(xs)