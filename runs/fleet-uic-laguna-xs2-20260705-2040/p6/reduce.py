import math

def parallel_sum(xs, nchunks):
    """Return bit-identical sum regardless of nchunks using math.fsum."""
    return math.fsum(xs)