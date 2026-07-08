import math

def parallel_sum(xs, nchunks):
    """
    Return a bit-identical sum regardless of chunk count.
    Uses math.fsum for exact floating-point summation (superaccumulator).
    """
    return math.fsum(xs)
