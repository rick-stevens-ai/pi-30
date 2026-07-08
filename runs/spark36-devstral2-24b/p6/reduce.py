import math

def parallel_sum(xs, nchunks):
    # Use a canonical ordering: sort by magnitude (absolute value) to ensure 
    # bit-identical results regardless of chunking scheme. This creates a fixed,
    # reproducible order for the sum operation.
    sorted_xs = sorted(xs, key=abs)
    return math.fsum(sorted_xs)