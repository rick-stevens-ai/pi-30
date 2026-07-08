import math


def parallel_sum(xs, nchunks):
    """Return the sum of xs using Kahan/fsum reduction so the result is
    bit-identical regardless of how many chunks are used to partition data.

    Strategy: always accumulate with math.fsum over the *whole* list in its
    original order.  The nchunks parameter is accepted (for API compatibility)
    but does not affect the reduction — every call produces the identical, 
    deterministic result that a single fsum(xs) would give.
    """
    return math.fsum(xs)
