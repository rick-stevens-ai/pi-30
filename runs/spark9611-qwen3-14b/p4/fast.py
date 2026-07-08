from decimal import Decimal, getcontext
import numpy as np

def softmax(x):
    getcontext().prec = 20  # Set precision for Decimal calculations
    x = [Decimal(val) for val in x]
    x_max = max(x)
    exps = [d.exp() for d in x]
    sum_exps = sum(exps)
    return [exp / sum_exps for exp in exps]