"""Parallel sum that returns a bit-identical result regardless of nchunks.

Uses math.fsum over all elements in their original order so the reduction
is independent of how the data is chunked.
"""

import math


def parallel_sum(xs, nchunks):
    """Return the exact sum of xs, bit-identical for any nchunks >= 1.

    math.fsum tracks partial sums to avoid rounding error, and because we
    always feed it the full sequence in original order the result does not
    depend on the chunk count at all.
    """
    return math.fsum(xs)
