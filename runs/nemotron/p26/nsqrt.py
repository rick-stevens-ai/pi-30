# P26 FIXED: Newton's method sqrt to full double precision.
# Handles 0 and 1 exactly. Uses frexp for good initial guess.
# Iterates until relative change < 2^-53 (double precision convergence).
# No math.sqrt used.
import math

def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    # frexp: x = m * 2^e, with 0.5 <= m < 1.0
    m, e = math.frexp(x)
    # Initial guess: sqrt(m) * 2^(e/2) ~= m * 2^(e//2) (since sqrt(m) ~ m for m in [0.5,1))
    # Better: use ldexp with exponent halved
    g = math.ldexp(m, e // 2)
    # If e is odd, multiply by sqrt(2) ~ 1.4142135623730951
    if e & 1:
        g *= 1.4142135623730951
    # Newton iterations until convergence (relative change < 2^-53)
    eps = 2.0**-53  # ~1.1e-16, double precision machine epsilon
    while True:
        g_new = 0.5 * (g + x / g)
        if abs(g_new - g) <= eps * g_new:
            return g_new
        g = g_new
