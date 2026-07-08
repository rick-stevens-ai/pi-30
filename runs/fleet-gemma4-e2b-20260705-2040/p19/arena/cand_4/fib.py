def fib(n: int) -> int:
    """
    Calculates the nth Fibonacci number using matrix exponentiation (O(log n)).
    fib(0) = 0, fib(1) = 1.
    Uses Python's native arbitrary-precision integers for large numbers.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1

    def multiply(A, B):
        """Multiplies two 2x2 matrices."""
        a, b = A[0][0], A[0][1]
        c, d = A[1][0], A[1][1]
        e, f = B[0][0], B[0][1]
        g, h = B[1][0], B[1][1]

        return [
            [a * e + b * g, a * f + b * h],
            [c * e + d * g, c * f + d * h]
        ]

    def power(M, p):
        """Computes M^p using binary exponentiation."""
        # Identity matrix for 2x2
        result = [[1, 0], [0, 1]]
        base = M

        while p > 0:
            if p % 2 == 1:
                result = multiply(result, base)
            base = multiply(base, base)
            p //= 2
        return result

    # The transition matrix T = [[1, 1], [1, 0]]
    T = [[1, 1], [1, 0]]

    # We need T^(n-1) to get F_n in the top-left (or equivalent calculation)
    # Since |F_n, F_{n-1}| = T^(n-1) * |F_1, F_0| = T^(n-1) * |1, 0|
    # The result F_n is the element at result[0][0] if we use F_1=1, F_0=0.
    # For n >= 1:
    # |F_{n+1}  F_n| = T^n * |F_1, F_0| = T^n * |1, 0|
    # If we compute T^n:
    final_matrix = power(T, n)

    # F_n is the element at (0, 1) or (1, 0) of the resulting matrix when starting from [F_1, F_0]
    # For M^n * [F_1, F_0]^T:
    # F_n = final_matrix[0][0]*F_1 + final_matrix[0][1]*F_0
    # Since F_1=1 and F_0=0, F_n = final_matrix[0][0] * 1 + final_matrix[0][1] * 0 = final_matrix[0][0]

    return final_matrix[0][0]

if __name__ == '__main__':
    # Test cases
    print(f"fib(0) = {fib(0)}")   # Expected: 0
    print(f"fib(1) = {fib(1)}")   # Expected: 1
    print(f"fib(2) = {fib(2)}")   # Expected: 1
    print(f"fib(3) = {fib(3)}")   # Expected: 2
    print(f"fib(10) = {fib(10)}") # Expected: 55
    print(f"fib(50) = {fib(50)}") # Test large number handling
    
    # Test a large N to check O(log n) performance and bigint support
    N_large = 200000
    import time
    start_time = time.perf_counter()
    result = fib(N_large)
    end_time = time.perf_counter()
    print(f"\nfib({N_large}) calculated.")
    print(f"Result length: {len(str(result))} digits")
    print(f"Calculation time for N={N_large}: {end_time - start_time:.6f} seconds")