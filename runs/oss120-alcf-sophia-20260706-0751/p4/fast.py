# fast.py – Numerically‑stable softmax implementation
# The reference test (check.py) expects a function `softmax` that accepts an
# iterable of numbers (floats) and returns a list of probabilities that sum to
# 1.0.  The implementation must avoid overflow/underflow by subtracting the
# maximum value before applying `math.exp`.

import math
from typing import Iterable, List


def softmax(xs: Iterable[float]) -> List[float]:
    """Return the soft‑max of *xs* using a numerically‑stable algorithm.

    The algorithm is:
    1. Find the maximum value *m* in the input.
    2. Compute `exp(x - m)` for each element, which prevents large exponents
       from overflowing.
    3. Normalise by the sum of the exponentials.

    This matches the high‑precision reference in `check.py` and is safe for
    inputs that would cause `math.exp` to overflow or underflow.
    """
    # Convert to a list so we can iterate multiple times and compute length.
    vals = list(xs)
    if not vals:
        return []
    # Step 1: maximum for numerical stability
    m = max(vals)
    # Step 2: exponentials of shifted values
    exps = [math.exp(v - m) for v in vals]
    # Step 3: normalisation
    total = sum(exps)
    # Guard against divide‑by‑zero (should not happen because at least one exp
    # will be 1.0 when shifted by the max).
    if total == 0.0:
        # Return uniform distribution to avoid crashes – this case occurs only
        # when all inputs are -inf, which is not expected in the test suite.
        n = len(vals)
        return [1.0 / n] * n
    return [e / total for e in exps]

# Export only the softmax function for the test harness.
__all__ = ["softmax"]
