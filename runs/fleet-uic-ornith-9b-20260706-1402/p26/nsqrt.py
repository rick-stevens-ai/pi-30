def nsqrt(x):
    if x == 0.0:
        return 0.0
    # Initial guess: max(1.0, x) gives a reasonable upper bound
    g = max(1.0, x)
    for _ in range(200):
        new_g = 0.5 * (g + x / g) if g != 0 else g
        # Convergence: relative change below tolerance
        if abs(new_g - g) <= 1e-14 * max(abs(g), 1e-308):
            return new_g
        g = new_g
    return g

# Keep backward-compatible name for converge_check.py
isqrt_newton = nsqrt
