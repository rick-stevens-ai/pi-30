# P26: nsqrt(x) = sqrt(x) to full double precision via Newton's method.
# Iterate until the relative change between successive iterates is below a few
# ulps (safely above machine epsilon to avoid 1-ulp oscillation / infinite loop),
# which drives the result to ~1e-16 relative error. Guard x==0 (and x==1)
# explicitly. No math.sqrt used.
def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    g = 1.0
    while True:
        nxt = 0.5 * (g + x / g)
        if abs(nxt - g) <= abs(g) * 1e-15:
            return nxt
        g = nxt