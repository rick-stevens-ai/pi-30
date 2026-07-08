import math

def softmax(xs):
    """Unstable softmax implementation (no max subtraction)."""
    if not xs:
        return []
    exps = [math.exp(x) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]
