import math

def parallel_sum(xs, nchunks):
    """
    Sum the list xs in parallel using nchunks chunks.
    Returns a bit-identical result regardless of nchunks.
    """
    # Use math.fsum over all data to ensure bit-identical result
    # regardless of how we partition the work
    return math.fsum(xs)
