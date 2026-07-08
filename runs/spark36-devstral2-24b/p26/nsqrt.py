import math

# P26: Newton's method for square root, iterates until convergence to full double precision.
def isqrt_newton(x):
    # Handle special cases
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    
    # Initial guess (log-based for better convergence over wide range)
    g = 1.0
    if x > 1.0:
        # For x > 1, use log2(x)/2 as initial estimate
        exponent = math.frexp(x)[1] - 1  # Get exponent of x
        g = 2 ** (exponent / 2)  # Initial guess based on exponent
    
    # Newton iteration until convergence
    for _ in range(100):
        prev_g = g
        g = 0.5 * (g + x / g)
        if abs(g - prev_g) < 1e-15:  # Converged to double precision
            break
    
    return g
