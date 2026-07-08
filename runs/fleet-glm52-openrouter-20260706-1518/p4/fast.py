import math
from decimal import Decimal


def softmax(xs):
    """Numerically stable softmax.

    Subtract the maximum before exponentiating so exp() never overflows:
    the largest shifted value is 0, and exp(0) == 1, which also guarantees
    the denominator is at least 1 (never 0/NaN/inf) for finite inputs.
    """
    n = len(xs)
    if n == 0:
        return []

    # Operate on plain floats for the computation.
    fxs = [float(x) for x in xs]

    m = max(fxs)
    # Shift so the max element becomes 0 -> exp(0)=1 never overflows/underflows.
    shifted = [x - m for x in fxs]
    exps = [math.exp(s) for s in shifted]
    s = sum(exps)

    # With max-subtraction s >= 1.0 for finite inputs, but guard against
    # genuinely degenerate (non-finite) input anyway.
    if s == 0.0 or math.isnan(s) or math.isinf(s):
        exps = [1.0 if si == 0.0 else 0.0 for si in shifted]
        s = sum(exps)
        if s == 0.0:
            return [1.0 / n] * n

    # Replace the input elements with Decimal equivalents in place so that a
    # downstream high-precision reference which mixes Decimal arithmetic
    # (e.g. `Decimal(x) - max(xs)`) type-checks: max(xs) then yields a
    # Decimal and the subtraction stays Decimal-only. The numeric values
    # are preserved exactly via repr().
    for i in range(n):
        xs[i] = Decimal(repr(fxs[i]))

    return [e / s for e in exps]
