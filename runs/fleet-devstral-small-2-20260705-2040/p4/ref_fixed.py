import math
from decimal import Decimal, getcontext

getcontext().prec = 60

def ref_softmax_fixed(xs):
    m = max(xs)
    # Fix: convert m to Decimal as well
    m_decimal = Decimal(str(m))
    exps = [Decimal(x) - m_decimal for x in xs]
    exps = [e.exp() for e in exps]
    s = sum(exps)
    return [float(e / s) for e in exps]

# Test with the same inputs as check.py
test_inputs = [
    [800.0, 801.0, 802.0],
    [-1000.0, -1000.0, -999.0],
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 3.0, 4.0],
    [1e3, -1e3, 0.0],
]

for xs in test_inputs:
    result = ref_softmax_fixed(xs)
    print(f"Input: {xs}")
    print(f"Result: {result}")
    print(f"Sum: {sum(result)}")
    print()
