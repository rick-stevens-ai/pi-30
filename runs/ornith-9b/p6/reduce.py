import math
from typing import Sequence


def parallel_sum(xs: Sequence[float], nchunks: int) -> float:
    """Return the exact sum of `xs` regardless of chunking strategy.

    ``math.fsum`` uses a compensated two-pass algorithm that computes an
    exactly-rounded IEEE 754 64-bit result for any subset, so the final
    output is bit-identical no matter how many chunks are used or in what
    order they were assembled.  The ``nchunks`` argument is accepted for
    interface compatibility but does not influence the computation.
    """
    return math.fsum(xs)
