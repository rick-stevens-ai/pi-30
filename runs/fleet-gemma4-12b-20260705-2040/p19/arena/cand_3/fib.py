def _fib(n):
    """
    Returns (F_n, F_{n+1}) using the fast doubling method.
    Complexity: O(log n) multiplications/additions of large integers.
    """
    if n == 0:
        return (0, 1)
    
    # Recursive step: find (F_k, F_{k+1}) where k = n // 2
    a, b = _fib(n // 2)
    
    # Fast doubling identities:
    # F_{2k}   = F_k * (2*F_{k+1} - F_k)
    # F_{2k+1} = F_{k+1}^2 + F_k^2
    c = a * (2 * b - a)
    d = a * a + b * b
    
    if n % 2 == 0:
        return (c, c + d)
    else:
        return (d, c + d)

def fib(n: int) -> int:
    """
    Returns the nth Fibonacci number.
    fib(0) = 0, fib(1) = 1.
    Uses fast doubling for O(log n) performance.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return _fib(n)[0]

if __name__ == "__main__":
    import sys
    # Increase the limit for integer to string conversion if needed, 
    # though not strictly required by the function itself.
    sys.set_int_max_str_digits(100000)
    
    test_cases = [0, 1, 2, 3, 4, 5, 10, 20]
    for n in test_cases:
        print(f"fib({n}) = {fib(n)}")
    
    # Performance check for n=200,000
    import time
    start = time.time()
    res = fib(200000)
    end = time.time()
    print(f"fib(200000) computed in {end - start:.4f} seconds")
    print(f"Number of digits: {len(str(res))}")
