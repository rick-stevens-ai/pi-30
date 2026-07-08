# P26 reflection: Newton's method square-root that must converge to full double
# precision for a wide range incl. tiny and huge inputs, and handle 0 exactly.
# Seed does a fixed 5 iterations from a bad initial guess -> fails for large x.
# Loop must iterate to convergence (and guard x==0), append lesson to memory.md.
from nsqrt import isqrt_newton
import math

def main():
    xs = [0.0, 1e-12, 1.0, 2.0, 1e6, 1e12, 1e18, 1234.5678, 0.25, 9.0]
    worst = 0.0
    for x in xs:
        got = isqrt_newton(x)
        exp = math.sqrt(x)
        if exp == 0:
            err = abs(got)
        else:
            err = abs(got - exp) / exp
        worst = max(worst, err)
        if math.isnan(got) or math.isinf(got):
            print(f"NAN/INF at x={x}: {got}")
            raise SystemExit(1)
    print(f"worst rel err = {worst:.3e}")
    if worst > 1e-12:
        print("NOT CONVERGED to double precision")
        raise SystemExit(1)
    print("OK P26")

if __name__ == "__main__":
    main()
