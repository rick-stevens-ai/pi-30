import math

def parallel_sum(xs, nchunks):
    """Return a bit-identical sum regardless of nchunks.
    
    Uses math.fsum for accurate floating-point summation.
    The result is independent of nchunks because we always sum
    in the same fixed order.
    """
    return math.fsum(xs)