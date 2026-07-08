
def isqrt_newton(x):
    if x == 0 or x == 1:
        return x
    guess = x / 2
    while True:
        next_guess = (guess + x / guess) / 2
        if abs(next_guess - guess) < max(1e-16, 1e-12 * guess):
            break
        guess = next_guess
    return guess
