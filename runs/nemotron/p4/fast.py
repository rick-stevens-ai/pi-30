import math
from decimal import Decimal, getcontext

getcontext().prec = 60

def softmax(xs):
    m = max(xs)
    exps = [Decimal(x - m).exp() for x in xs]
    sum_exps = sum(exps)
    return [float(e / sum_exps) for e in exps]
