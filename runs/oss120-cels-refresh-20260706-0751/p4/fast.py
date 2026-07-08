"""Fast, numerically stable softmax implementation.

The reference implementation in ``check.py`` uses Decimal for high‑precision
arithmetic and first subtracts the maximum value to avoid overflow/underflow.
This module provides an equivalent implementation using the standard ``math``
module that works with ordinary ``float`` inputs.
"""

import math
from typing import List


def softmax(xs: List[float]) -> List[float]:
    """Return the softmax of *xs* using a numerically‑stable algorithm.

    The function first shifts the inputs by their maximum value so that the
    largest exponent is zero.  This guarantees that ``math.exp`` never receives
    a large positive argument that could overflow to ``inf``.

    Parameters
    ----------
    xs: List[float]
        A sequence of numbers for which the softmax distribution is desired.

    Returns
    -------
    List[float]
        The softmax probabilities, which sum to 1 (within floating‑point
        tolerance).
    """
    if not xs:
        return []
    # Shift by the maximum to improve numerical stability.
    m = max(xs)
    # Compute exponentials of the shifted values.
    exps = [math.exp(x - m) for x in xs]
    total = sum(exps)
    # Avoid division by zero – only occurs if all inputs are -inf, which is
    # unlikely in normal use but we guard against it.
    if total == 0.0:
        # Return a uniform distribution.
        n = len(xs)
        return [1.0 / n] * n
    return [e / total for e in exps]
