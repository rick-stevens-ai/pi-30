def fib(n: int) -> int:
    """
    Computes the nth Fibonacci number using the fast-doubling method.
    Time complexity: O(log n) multiplications.
    Space complexity: O(log n) to store the result (bigint).

    Args:
        n: The index of the Fibonacci number to compute (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Fast doubling method:
    # F(2k) = F(k) * (2*F(k+1) - F(k))
    # F(2k+1) = F(k+1)^2 + F(k)^2
    
    # We iterate through the bits of n from most significant to least significant.
    # Starting with F(0) and F(1).
    a, b = 0, 1  # a = F(i), b = F(i+1)
    
    # bin(n)[2:] gives the binary representation without '0b' prefix.
    for bit in bin(n)[2:]:
        c = a * (2 * b - a)
        d = a * a + b * b
        if bit == '1':
            a, b = d, c + d
        else:
            a, b = c, d
    
    return a

if __name__ == "__main__":
    # Test cases
    test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for i, expected_val in enumerate(expected):
        result = fib(i)
        assert result == expected_val, f"Error at n={i}: expected {expected_val}, got {result}"
    print("Small test cases passed.")

    # Large test case: n=200000 (should be fast)
    import time
    start = time.time()
    res = fib(200000)
    end = time.time()
    print(f"fib(200000) computed in {end - start:.4f} seconds.")
    # Check length of the result to ensure it's a large number
    print(f"Length of fib(200000): {len(str(res))} digits")
