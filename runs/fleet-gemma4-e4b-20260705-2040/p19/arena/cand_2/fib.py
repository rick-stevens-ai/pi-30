def fib(n):
    """
    Calculates the nth Fibonacci number using fast doubling (O(log n)).

    Args:
        n (int): The index of the Fibonacci number to calculate (n >= 0).

    Returns:
        int: The nth Fibonacci number as a Python bigint.
    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Fast Doubling implementation based on identities:
    # F(2k) = F(k) * (2*F(k+1) - F(k))
    # F(2k+1) = F(k+1)^2 + F(k)^2

    def fib_pair(k):
        """Returns the pair (F(k), F(k+1))."""
        if k == 0:
            return (0, 1)  # (F(0), F(1))
        
        a, b = fib_pair(k // 2)
        
        # Calculate F(k/2) and F(k/2 + 1)
        f_k_half = a
        f_k_plus_1_half = b

        if k % 2 == 0:
            # k is even, k = 2*m. We have (F(m), F(m+1)) where m=k/2
            # F(2m) = F(m) * (2*F(m+1) - F(m))
            f_2m = f_k_half * (2 * f_k_plus_1_half - f_k_half)
            # F(2m+1) = F(m+1)^2 + F(m)^2
            f_2m_plus_1 = f_k_plus_1_half**2 + f_k_half**2
            return (f_2m, f_2m_plus_1)
        else:
            # k is odd, k = 2*m + 1. We have (F(m), F(m+1)) where m=(k-1)/2
            # Let m' = (k-1)/2. We want F(k) and F(k+1).
            # It's easier to use the property that if we calculate for k-1 (which is even), 
            # we get F(k-1) and F(k).

            # Let's stick to calculating F(k) and F(k+1) directly from F(m) and F(m+1) where m = floor(k/2).
            
            # If k is odd, let k = 2m + 1. We use the identities for 2m and 2m+1.
            # We calculate (F(2m), F(2m+1)) first using m.
            f_2m, f_2m_plus_1 = fib_pair(k - 1) # Recursively call for k-1 which is even

            # F(k) = F(2m+1)
            # F(k+1) = F(2m+2)
            
            # Using the identities derived from matrix exponentiation:
            # (F(k), F(k+1)) = (F(floor(k/2)), F(ceil(k/2))) * M^(floor(k/2))

            # Let's simplify and use the definition based on m=k//2.
            m = k // 2
            f_m, f_m_plus_1 = fib_pair(m)

            if k % 2 == 0: # k = 2m
                F_2m = f_m * (2 * f_m_plus_1 - f_m)
                F_2m_plus_1 = f_m_plus_1**2 + f_m**2
                return (F_2m, F_2m_plus_1)
            else: # k = 2m + 1
                # We need F(k) and F(k+1).
                # F(2m+1) = F(m)^2 + F(m+1)^2
                F_2m_plus_1 = f_m**2 + f_m_plus_1**2

                # F(2m+2) = F(m+1)^2 + 2*F(m)*F(m+1)
                F_2m_plus_2 = f_m_plus_1**2 + 2 * f_m * f_m_plus_1

                return (F_2m_plus_1, F_2m_plus_2)


    # We want F(n), which is the first element of fib_pair(n).
    result, _ = fib_pair(n)
    return result

if __name__ == "__main__":
    import sys
    sys.set_int_max_str_digits(sys.maxsize)
    import time

    print("--- Testing Fibonacci Fast Doubling ---")

    # Test small values
    tests = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13}
    all_passed = True
    for n, expected in tests.items():
        result = fib(n)
        assert result == expected, f"Test failed for n={n}. Expected {expected}, got {result}"
        print(f"fib({n}) = {result}")

    # Test large value (N=200000)
    N_large = 200000
    start_time = time.perf_counter()
    try:
        F_N_large = fib(N_large)
        end_time = time.perf_counter()
        print(f"\nSuccessfully calculated F({N_large}).")
        # Printing the first 50 digits to verify it's a large number
        print(f"F({N_large}) starts with: {str(F_N_large)[:50]}...")
        print(f"Calculation time: {(end_time - start_time)*1000:.2f} ms")

    except RecursionError as e:
        print(f"\nERROR: Recursion depth exceeded for N={N_large}. The implementation might be flawed or Python's recursion limit is too low.")
    
    # Check if the result type supports bigint (Python integers do by default)
    if isinstance(F_N_large, int):
        print("\nResult type confirmed to support arbitrary precision (bigint).")

