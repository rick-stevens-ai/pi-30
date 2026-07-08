import math
import numpy as np

def reduce_sum(xs):
    # Convert to a well-defined type array and sort for consistent sum order
    xs = np.asarray(xs, dtype=np.float64)
    return math.fsum(np.sort(xs))

def parallel_sum(xs, nchunks=1):
    # BIT-IDENTICAL regardless of nchunks: sort all data and fsum once.
    # nchunks is ignored; sorting gives a deterministic order independent of chunking.
    xs = np.asarray(xs, dtype=np.float64)
    return math.fsum(np.sort(xs))
