# Implementation of numerically stable softmax
import math

def softmax(xs):
    """Return a softmax of xs in a numerically stable way.

    The function subtracts the maximum value from each element before exponentiation
    to avoid overflow. This mirrors the reference implementation that uses Decimal
    for higher precision but retains the familiar math.exp path for speed.

    All outputs are floats and the probabilities sum to 1.0 (subject to float
    rounding). The result list preserves the order of ``xs``.
    """
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    # Guard against extremely small sums due to underflow; this should not
    # happen because we subtracted the maximum, but the guard keeps the function
    # robust on pathological inputs.
    if s == 0.0:
        # In the unlikely event of total underflow return a uniform distribution
        n = len(xs)
        return [1.0 / n] * n
    return [e / s for e in exps]
