# P26: Fixed Newton iteration to converge to full double precision using while loop and proper guard for 0.
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
