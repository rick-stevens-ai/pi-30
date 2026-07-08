import math
from decimal import Decimal, getcontext

getcontext().prec = 60

def softmax(xs):
    """Numerically stable softmax implementation using Decimal for precision."""
    if not xs:
        return []
    # Subtract max for numerical stability (prevents overflow)
    m = max(xs)
    # Convert to Decimal for precise arithmetic
    m_decimal = Decimal(str(m))
    exps = [Decimal(str(x)) - m_decimal for x in xs]
    exps = [e.exp() for e in exps]
    s = sum(exps)
    return [float(e / s) for e in exps]
