import math

def softmax(xs):
    xs = [float(x) for x in xs]
    mx = max(xs)
    exps = [math.exp(x - mx) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]
