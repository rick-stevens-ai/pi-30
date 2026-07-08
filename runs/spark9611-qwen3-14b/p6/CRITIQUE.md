NO_ISSUES

The result does not depend on nchunks because math.fsum(xs) sums the entire list regardless of chunking. FP operations are deterministic via math.fsum.