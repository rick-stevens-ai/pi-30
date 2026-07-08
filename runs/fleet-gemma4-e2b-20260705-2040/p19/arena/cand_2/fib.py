def fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using matrix exponentiation (fast doubling, O(log n)).
    fib(0) = 0, fib(1) = 1.
    Uses standard library only and handles large integers (bigint).
    """
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1

    def multiply(A, B):
        # Multiplies two 2x2 matrices
        a, b = A[0][0], A[0][1]
        c, d = A[1][0], A[1][1]
        e, f = B[0][0], B[0][1]
        g, h = B[1][0], B[1][1]

        new_a = a * e + b * g
        new_b = a * f + b * h
        new_c = c * e + d * g
        new_d = c * f + d * h
        return [[new_a, new_b], [new_c, new_d]]

    def power(M, n):
        # Computes M^n using exponentiation by squaring
        result = [[1, 0], [0, 1]]  # Identity matrix
        base = M
        while n > 0:
            if n % 2 == 1:
                result = multiply(result, base)
            base = multiply(base, base)
            n //= 2
        return result

    # The transformation matrix M = [[1, 1], [1, 0]]
    M = [[1, 1], [1, 0]]

    # F(n) is found using the formula: | F(n) | = M^(n-1) * | F(1) |
    # Since F(1)=1 and F(0)=0. We compute M^(n-1)
    M_pow = power(M, n - 1)

    # F(n) is the top-left element of the resulting vector calculation:
    # [F(n), F(n-1)]^T = M^(n-1) * [F(1), F(0)]^T = M^(n-1) * [1, 0]^T
    # This means F(n) is the element at M_pow[0][0] * 1 + M_pow[0][1] * 0 = M_pow[0][0]
    return M_pow[0][0]

if __name__ == '__main__':
    # Test cases
    print(f"fib(0) = {fib(0)}") # Expected: 0
    print(f"fib(1) = {fib(1)}") # Expected: 1
    print(f"fib(2) = {fib(2)}") # Expected: 1
    print(f"fib(3) = {fib(3)}") # Expected: 2
    print(f"fib(10) = {fib(10)}") # Expected: 55
    # Test a larger number to check bigint and speed (though timing is not required)
    N = 100000
    import time
    start_time = time.time()
    result = fib(N)
    end_time = time.time()
    print(f"fib({N}) calculated in {end_time - start_time:.6f} seconds.")
    # print(f"fib({N}) has {len(str(result))} digits.") # For verification of bigint handling