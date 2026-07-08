def fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using matrix exponentiation (O(log n)).
    fib(0) = 0, fib(1) = 1. Handles arbitrary precision integers (bigint).
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Base transformation matrix M = [[1, 1], [1, 0]]
    M = [[1, 1], [1, 0]]

    def multiply(A, B):
        """Multiplies two 2x2 matrices."""
        a, b = A[0]
        c, d = A[1]
        e, f = B[0]
        g, h = B[1]

        new_a = a * e + b * g
        new_b = a * f + b * h
        new_c = c * e + d * g
        new_d = c * f + d * h

        return [[new_a, new_b], [new_c, new_d]]

    def power(M, p):
        """Calculates M^p using exponentiation by squaring (fast doubling)."""
        # Identity matrix for 2x2
        result = [[1, 0], [0, 1]]
        base = M

        while p > 0:
            # If p is odd, multiply the result by the current base
            if p % 2 == 1:
                result = multiply(result, base)
            
            # Square the base matrix and halve p
            base = multiply(base, base)
            p //= 2
        
        return result

    # We need M^(n-1) to get F(n) from the standard setup:
    # [[F(n), F(n-1)], [F(n-1), F(n-2)]] = M^(n-1)
    M_pow = power(M, n - 1)

    # F(n) is the top-left element of M^(n-1) * [[F(1)], [F(0)]] = M^(n-1) * [[1], [0]]
    # F(n) = M_pow[0][0] * 1 + M_pow[0][1] * 0
    return M_pow[0][0]

if __name__ == '__main__':
    # Test cases
    print(f"fib(0) = {fib(0)}")   # Expected: 0
    print(f"fib(1) = {fib(1)}")   # Expected: 1
    print(f"fib(7) = {fib(7)}")   # Expected: 13
    print(f"fib(10) = {fib(10)}") # Expected: 55
    
    # Test a large number to verify speed and bigint handling
    n_large = 200000
    import time
    start_time = time.perf_counter()
    result = fib(n_large)
    end_time = time.perf_counter()
    print(f"fib({n_large}) calculated in {end_time - start_time:.4f} seconds.")
    # print(f"First 50 digits of fib({n_large}): {str(result)[:50]}...") # Uncomment to see result
