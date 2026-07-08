def fib(n):
    """
    Calculates the nth Fibonacci number using fast-doubling method (O(log n)).
    Uses exact Python bigint for arbitrary precision integers.
    Assumes fib(0)=0 and fib(1)=1.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Fast doubling implementation based on properties of Fibonacci numbers:
    # F(2k) = F(k) * (2*F(k+1) - F(k))
    # F(2k+1) = F(k+1)^2 + F(k)^2

    def fib_recursive(k):
        if k == 0:
            return 0
        if k == 1:
            return 1
        
        if k % 2 == 0:
            # k = 2m => m = k // 2
            m = k // 2
            f_m = fib_recursive(m)
            f_m_plus_1 = fib_recursive(m + 1)
            return f_m * (2 * f_m_plus_1 - f_m)
        else:
            # k = 2m + 1 => m = (k - 1) // 2
            m = (k - 1) // 2
            f_m = fib_recursive(m)
            f_m_plus_1 = fib_recursive(m + 1)
            return f_m_plus_1**2 + f_m**2

    return fib_recursive(n)

if __name__ == '__main__':
    # Test cases
    print(f"fib(0) = {fib(0)}") # Expected: 0
    print(f"fib(1) = {fib(1)}") # Expected: 1
    print(f"fib(2) = {fib(2)}") # Expected: 1
    print(f"fib(3) = {fib(3)}") # Expected: 2
    print(f"fib(5) = {fib(5)}") # Expected: 5

    # Test for large number (n=200000) - verification of performance and bigint capability
    N_large = 200000
    print(f"\nCalculating fib({N_large})... This might take a moment.")
    try:
        result_large = fib(N_large)
        # Print the number of digits to confirm large integer handling, but avoid printing the massive number itself.
        print(f"fib({N_large}) calculated successfully.")
        print(f"Number of digits in result: {len(str(result_large))}")
    except RecursionError as e:
        # If recursion depth is hit for very large N, we might need to switch to iterative memoization or matrix exponentiation approach.
        print(f"\nWarning: Calculation failed due to recursion limit: {e}. The implementation relies on recursion depth being manageable for O(log n).")

    # A quick check for a smaller but still challenging number
    N_medium = 1000
    result_medium = fib(N_medium)
    print(f"\nfib({N_medium}) calculated successfully. Number of digits: {len(str(result_medium))}")