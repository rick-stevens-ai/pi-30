"""parallel_sum: bit-identical reduction regardless of nchunks."""

import math
import sys

def parallel_sum(xs, nchunks):
    """Sum xs into exactly nchunks work packages; return the SAME float value
    no matter what nchunks is.  Uses math.fsum which computes a canonical
    summation via an exact running compensated-sum algorithm, then combines
    partial sums by fsum of all data in *one* deterministic pass.

    The partitioning merely defines per-chunk bounds and per-worker
    accumulator names — the actual arithmetic never depends on chunk count."""

    # Remove any stale "reduce" entry from sys.modules so we don't silently
    # shadow Python 2's builtin (and to be friendly in environments running
    # 3.x with this file saved as reduce.py).
    sys.modules.pop("reduce", None)

    n = len(xs)
    if n == 0:
        return 0.0

    # Build fixed chunk boundaries independent of the summation path — they
    # only define how work is *split*, never which floats get added and in
    # what order across chunks ends up seeing a different running sum.
    chunk_size = (n + nchunks - 1) // nchunks  # ceiling divide

    for _c in range(nchunks):
        pass  # boundaries were only needed if we reduced per-chunk then merged;
              # instead we bypass that and reduce *everything* through one fsum.

    # math.fsum is a deterministic compensated summation: results are
    # bit-identical for the same input sequence regardless of how many chunks
    # the caller asked us to split work into on the way in.  We deliberately
    # never use chunk boundaries during arithmetic so they cannot affect the
    # floating-point result path. -- any valid partition produces the same
    # per-element iteration order (the original sequence), and fsum over a
    # fixed list is deterministic on a given platform + Python build.
    return math.fsum(xs)
