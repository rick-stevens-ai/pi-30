def isqrt_newton(x):
    if x == 0:
        return 0.0
    g = x if x > 1 else 1.0
    while True:
        next_g = 0.5 * (g + x / g)
        if next_g == g:
            break
        g = next_g
    return g

import math
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
print(f"worst rel err = {worst:.3e}")
