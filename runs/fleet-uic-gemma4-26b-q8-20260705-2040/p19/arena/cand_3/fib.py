def fib(n):
    """
    Computes the nth Fibonacci number using the fast doubling method.
    Complexity: O(log n) multiplications.
    Python's arbitrary-precision integers are used.
    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")
    if n == 0:
        return 0

    # Binary expansion of n
    bin_n = bin(n)[2:]
    
    a, b = 0, 1  # Represents (F_i, F_{i+1}) starting with i=0
    for bit in bin_n:
        # Double the index: i -> 2i
        # F_{2k} = F_k * (2*F_{k+1} - F_k)
        # F_{2k+1} = F_{k+1}^2 + F_k^2
        c = a * (b * 2 - a)
        d = a * a + b * b
        a, b = c, d
        
        if bit == '1':
            # Increment the index: 2i -> 2i+1
            # Since we're at 2i, adding 1 takes us to (F_{2i+1}, F_{2i+2})
            # where F_{2i+2} = F_{2i} + F_{2i+1}
            a, b = b, a + b
            
    return a

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            print(fib(n))
        except ValueError:
            print("Please provide an integer.")
