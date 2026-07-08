import math


def softmax(xs):
    """Compute the numerically‑stable softmax of a numeric iterable.

    The implementation subtracts the maximum input value ``m`` before computing
    exponents, which prevents overflow/underflow on large or small inputs.  It
    returns a list of floats that sum to one (up to floating point precision).
    """
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    sum_exps = sum(exps)
    # If underflow leads to zero or NaN, return zeros to avoid NaNs in output.
    if not sum_exps or math.isnan(sum_exps):
        return [0.0] * len(xs)
    inv_sum = 1.0 / sum_exps
    return [e * inv_sum for e in exps]
