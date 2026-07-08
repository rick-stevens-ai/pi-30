import math

def softmax(xs):
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]
