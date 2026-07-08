from decimal import Decimal


def softmax(xs):
    m = Decimal(max(xs))
    exps = [Decimal(x - m).exp() for x in [Decimal(v) for v in xs]]
    s = sum(exps)
    return [float(e / s) for e in exps]
