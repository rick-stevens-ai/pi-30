def fib(n):
    """
    Compute the nth Fibonacci number using the fast doubling method.
    F(0) = 0, F(1) = 1.
    Complexity: O(log n) multiplications of large integers.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # Fast doubling formulas:
    # F_{2k} = F_k * (2*F_{k+1} - F_k)
    # F_{2k+1} = F_{k+1}^2 + F_k^2

    a, b = 0, 1  # a = F_k, b = F_{k+1}
    # Process bits of n from most significant to least significant.
    # bin(n) returns '0b...' so we skip the first two characters.
    for bit in bin(n)[2:]:
        # k -> 2k
        f_2k = a * ((b << 1) - a)
        f_2kplus1 = a * a + b * b
        
        if bit == '0':
            a, b = f_2k, f_2kplus1
        else:
            # k -> 2k+1
            # F_{2k+1} is already computed as f_2kplus1.
            # F_{2k+2} = F_{2k} + F_{2k+1}.
            a, b = f_2kplus1, f_2k + f_2kplus1

    return a
