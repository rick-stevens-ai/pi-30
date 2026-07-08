# fast.py – numerically stable softmax implementation
# This module provides a softmax function that is safe against overflow and underflow.
# It subtracts the maximum value from the inputs before applying the exponential,
# which is the standard technique for numerical stability.

import math
from typing import Iterable, List


def softmax(xs: Iterable[float]) -> List[float]:
    """Return the softmax of the sequence *xs*.

    The implementation is numerically stable: it first subtracts the maximum
    value from each element to avoid overflow in ``math.exp``.  It works for
    empty inputs (returns an empty list) and for any iterable of real numbers.
    """
    # Convert the input to a list so we can traverse it multiple times.
    arr = list(xs)
    if not arr:
        return []

    # Find the maximum value to shift the inputs.
    m = max(arr)
    # Compute exponentials of the shifted values.
    exps = [math.exp(x - m) for x in arr]
    total = sum(exps)
    # Guard against a total of zero (should not happen with the shift, but
    # retain a safe fallback).  In that pathological case, return a uniform
    # distribution.
    if total == 0.0:
        n = len(arr)
        return [1.0 / n] * n
    return [e / total for e in exps]
