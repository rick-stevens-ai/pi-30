import math

def parallel_sum(xs, nchunks):
    """
    Return the sum of xs using math.fsum, which is independent of chunking.
    The nchunks argument is ignored to ensure bit-identical results.
    """
    if nchunks <= 0:
        raise ValueError("nchunks must be positive")
    return math.fsum(xs)
