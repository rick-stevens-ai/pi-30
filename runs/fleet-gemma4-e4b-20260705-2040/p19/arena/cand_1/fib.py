def multiply(A, B):
    # Matrix multiplication for 2x2 matrices
    a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
    e, f, g, h = B[0][0], B[0][1], B[1][0], B[1][1]
    return [
        [a*e + b*g, a*f + b*h],
        [c*e + d*g, c*f + d*h]
    ]

def power(M, n):
    # Matrix exponentiation by squaring (O(log n))
    result = [[1, 0], [0, 1]]  # Identity matrix
    base = M
    while n > 0:
        if n % 2 == 1:
            result = multiply(result, base)
        base = multiply(base, base)
        n //= 2
    return result

def fib(n):
    """
    Calculates the nth Fibonacci number using matrix exponentiation (O(log n)).

    Args:
        n (int): The index of the Fibonacci number (n >= 0).

    Returns:
        int: The nth Fibonacci number, using exact Python big integers.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # The base matrix Q = [[1, 1], [1, 0]]
    Q = [[1, 1], [1, 0]]
    
    # We calculate Q^n. 
    # Q^n = [[F_{n+1}, F_n], [F_n, F_{n-1}]]
    M = power(Q, n)
    return M[1][0]

if __name__ == '__main__':
    import time

    # Test small values
    print(f"fib(0): {fib(0)}") # Expected: 0
    print(f"fib(1): {fib(1)}") # Expected: 1
    print(f"fib(2): {fib(2)}") # Expected: 1
    print(f"fib(3): {fib(3)}") # Expected: 2
    print(f"fib(4): {fib(4)}") # Expected: 3

    # Test large value (n=200000) to verify speed and big integer handling
    N = 200000
    print(f"\nCalculating fib({N})...")
    start_time = time.time()
    result = fib(N)
    end_time = time.time()

    # Print the result (or just its size/last few digits if it's too long)
    print(f"fib({N}) calculated successfully. Result length: {len(str(result))} digits.")
    print(f"Time taken for fib({N}): {end_time - start_time:.4f} seconds.")