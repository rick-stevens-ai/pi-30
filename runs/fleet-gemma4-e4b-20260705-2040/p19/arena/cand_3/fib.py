def multiply(A, B):
    """Multiplies two 2x2 matrices."""
    a, b = A[0]
    c, d = A[1]
    e, f = B[0]
    g, h = B[1]

    # Matrix multiplication: C[i][j] = sum(A[i][k] * B[k][j])
    return [
        [a*e + b*g, a*f + b*h],
        [c*e + d*g, c*f + d*h]
    ]

def matrix_pow(M, n):
    """Computes M^n using exponentiation by squaring."""
    # Identity matrix for 2x2
    result = [[1, 0], [0, 1]]
    base = M

    while n > 0:
        # If n is odd, multiply the result with the current base
        if n % 2 == 1:
            result = multiply(result, base)
        
        # Square the base matrix
        base = multiply(base, base)
        
        # Halve n
        n //= 2
    return result

def fib(n):
    """
    Calculates the nth Fibonacci number using matrix exponentiation (O(log n)).
    fib(0)=0, fib(1)=1. Uses exact Python bigints.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # The Fibonacci recurrence relation can be expressed using the matrix:
    # [[F(n+1)], [F(n)]] = [[1, 1], [1, 0]]^n * [[F(1)], [F(0)]]
    
    # We need to calculate M^(n-1) where M = [[1, 1], [1, 0]].
    # The result F_n will be the element at position [1][0] of M^n * [1, 0]^T.
    # A simpler approach is to use M^n and take the bottom left element F(n) if we start with (F2, F1).
    # Let's stick to calculating M^(n-1) and then using the property:
    # [[F_n], [F_{n-1}]] = [[1, 1], [1, 0]]^(n-1) * [[F_1], [F_0]] = [[1, 1], [1, 0]]^(n-1) * [[1], [0]]
    
    # However, calculating M^n directly is cleaner:
    # M^n = [[F_{n+1}, F_n], [F_n, F_{n-1}]]
    
    M = [[1, 1], [1, 0]]
    Mn = matrix_pow(M, n)
    
    # F_n is the element at Mn[1][0] (or Mn[0][1])
    return Mn[1][0]

if __name__ == '__main__':
    import sys
    
    try:
        if len(sys.argv) != 2:
            print("Usage: python fib.py <n>")
            sys.exit(1)
            
        n = int(sys.argv[1])
        result = fib(n)
        print(f"fib({n}) = {result}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)