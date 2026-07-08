# P26 SEED: fixed dynamic Newton iterations until convergence.
def isqrt_newton(x):
    if x < 0:
        raise ValueError("nsqrt is not defined for negative numbers")
    if x == 0 or x == 1:
        return x
    # Initial guess adaptation
    guess = x / 2.0 if x >= 1.0 else 1.0
    while True:
        new_guess = 0.5 * (guess + x / guess)
        # Check for convergence to double precision
        if abs(new_guess - guess) <= 1e-14 * max(1.0, abs(new_guess)):
            return new_guess
        guess = new_guess