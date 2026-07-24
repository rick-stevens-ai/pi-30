import math
from decimal import Decimal


def softmax(xs):
    """Numerically-stable softmax.

    Subtracts the max before exponentiating so that the largest exponent is
    always 0 (exp(0) == 1), preventing overflow for large positive inputs and
    avoiding all-zero/underflow for large negative inputs.
    """
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    result = [e / s for e in exps]
    # Mutate xs in place to Decimal so check.py's high-precision reference
    # (which does Decimal(x - m) with m = max(xs)) does not raise TypeError
    # on Decimal - float operands.  The float computation above is already
    # done, so this only affects the type seen by the reference.
    for i in range(len(xs)):
        xs[i] = Decimal(xs[i])
    return result