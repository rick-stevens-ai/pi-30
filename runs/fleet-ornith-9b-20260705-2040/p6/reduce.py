import math


def parallel_sum(xs, nchunks):
    """Return a bit-identical sum of xs regardless of nchunks."""
    return float(math.fsum(xs))
