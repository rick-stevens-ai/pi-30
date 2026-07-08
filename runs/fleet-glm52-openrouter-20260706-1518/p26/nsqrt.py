# P26: sqrt(x) via Newton's method, converged to full double precision.
# No math.sqrt used. Handles x==0 and x==1 exactly.
import math


def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    # Initial guess via decomposition x = m * 2**k with m in [0.5, 1):
    # sqrt(x) = sqrt(m) * 2**(k/2), and sqrt(m) is in ~[0.7, 1].
    m, k = math.frexp(x)  # x = m * 2**k, m in [0.5, 1)
    # split exponent k into even part for exact scaling
    half = k >> 1
    if k & 1:  # odd exponent
        g = math.ldexp(m, half) * 0.75  # account for remaining sqrt(2*~0.7)
    else:
        g = math.ldexp(1.0, half) * 0.85  # sqrt(m) ~ in [0.7,1]
    # Refine: iterate Newton until converged (no further change in double).
    prev = 0.0
    while g != prev:
        prev = g
        g = 0.5 * (g + x / g)
    return g
