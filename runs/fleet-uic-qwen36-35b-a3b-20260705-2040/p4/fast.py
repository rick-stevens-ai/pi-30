import math


def softmax(xs):
    """Numerically stable softmax: subtract max before taking exp."""
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]
