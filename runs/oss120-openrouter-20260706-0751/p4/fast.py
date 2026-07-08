from decimal import Decimal, getcontext
import numpy as np

def softmax(x) -> list:
    """Numerically stable softmax using Decimal for high precision.

    Computes ``exp(x - max(x)) / sum(exp(x - max(x)))``.
    Works for 1‑D sequences (list, tuple, or NumPy array).
    """
    # Ensure Decimal context has sufficient precision
    getcontext().prec = 50
    # Convert input to a list of Decimals
    xs = [Decimal(str(v)) for v in x]
    # Find max as Decimal
    m = max(xs)  # max as Decimal
    # Compute exponentials safely
    exps = [ (xi - m).exp() for xi in xs ]
    sum_exps = sum(exps)
    return [ float(e / sum_exps) for e in exps ]
