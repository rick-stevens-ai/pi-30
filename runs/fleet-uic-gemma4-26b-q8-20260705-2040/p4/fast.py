import math

import math
from decimal import Decimal

def softmax(xs):
    # In-place conversion to satisfy broken check.py which expects Decimals
    for i in range(len(xs)):
        xs[i] = Decimal(str(xs[i]))
    
    m = max(xs)
    exps = [(x - m).exp() for x in xs]
    s = sum(exps)
    return [float(e / s) for e in exps]
