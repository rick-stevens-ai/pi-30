# P8 convergence check — DO NOT let the agent edit this file.
# integrator.solve(f, y0, t0, t1, n) integrates dy/dt = f(t,y).
# Test: dy/dt = y, y(0)=1 -> y(t)=e^t. With many steps the error must be tiny.
# Classic trap: accumulating t += h drifts; compute t = t0 + step*h instead,
# and use a stable scheme (RK4) so error shrinks with step count.
import math
from integrator import solve

def main():
    f = lambda t, y: y
    y0, t0, t1 = 1.0, 0.0, 1.0
    n = 50000
    y = solve(f, y0, t0, t1, n)
    exact = math.e
    err = abs(y - exact)
    print(f"y({t1})={y:.12f} exact={exact:.12f} err={err:.3e}")
    if err > 1e-6:
        print("NOT CONVERGED")
        raise SystemExit(1)
    # second test: dy/dt = -2*t*y  (y = exp(-t^2)), check t accumulation drift
    g = lambda t, y: -2.0 * t * y
    y2 = solve(g, 1.0, 0.0, 3.0, 60000)
    exact2 = math.exp(-9.0)
    err2 = abs(y2 - exact2)
    print(f"gaussian y(3)={y2:.3e} exact={exact2:.3e} err={err2:.3e}")
    if err2 > 1e-6:
        print("NOT CONVERGED (drift)")
        raise SystemExit(1)
    print("OK converged")

if __name__ == "__main__":
    main()
