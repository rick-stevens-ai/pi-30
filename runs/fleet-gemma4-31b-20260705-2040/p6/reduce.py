import math

def parallel_sum(xs, nchunks):
    """
    Computes the sum of xs. To ensure bit-identical results regardless of 
    nchunks, we use math.fsum which provides high precision and a consistent 
    result for a given input sequence.
    """
    return math.fsum(xs)
