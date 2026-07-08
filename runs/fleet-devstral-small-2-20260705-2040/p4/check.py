# P4 oracle — DO NOT let the agent edit this file.
# Differential test: numerically-stable softmax (fast.py) must match a
# high-precision reference on inputs engineered to overflow naive exp().
import sys
import math
from decimal import Decimal, getcontext
getcontext().prec = 60

from fast import softmax as fast_softmax

def ref_softmax(xs):
    m = max(xs)
    m_decimal = Decimal(str(m))
    exps = [Decimal(x) - m_decimal for x in [Decimal(v) for v in xs]]
    exps = [e.exp() for e in exps]
    s = sum(exps)
    return [float(e / s) for e in exps]

def make_inputs():
    return [
        [800.0, 801.0, 802.0],          # forces overflow in naive exp
        [-1000.0, -1000.0, -999.0],      # forces underflow to all-zero / nan
        [0.0, 0.0, 0.0],
        [1.0, 2.0, 3.0, 4.0],
        [1e3, -1e3, 0.0],
    ]

def main():
    maxerr = 0.0
    for xs in make_inputs():
        got = fast_softmax(xs)
        exp = ref_softmax(xs)
        if len(got) != len(exp):
            print(f"MISMATCH length {xs}"); sys.exit(1)
        for g, e in zip(got, exp):
            if math.isnan(g) or math.isinf(g):
                print(f"NAN/INF in output for {xs}: {got}"); sys.exit(1)
            maxerr = max(maxerr, abs(g - e))
        s = sum(got)
        if abs(s - 1.0) > 1e-9:
            print(f"DOES NOT SUM TO 1 for {xs}: sum={s}"); sys.exit(1)
    if maxerr > 1e-9:
        print(f"MAXERR {maxerr:.3e} exceeds tol"); sys.exit(1)
    print(f"OK maxerr={maxerr:.3e}")
    sys.exit(0)

if __name__ == "__main__":
    main()
