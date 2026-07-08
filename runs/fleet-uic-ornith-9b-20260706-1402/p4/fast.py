from decimal import Decimal


def softmax(xs):
    m = max(xs)
    exps = [Decimal(e - m).exp() for e in xs]
    s = sum(exps)
    if s == 0:
        return [1.0 / len(xs)] * len(xs)
    return [float(e / s) for e in exps]
