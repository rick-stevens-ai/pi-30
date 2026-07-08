def fib(n):
    """
    Returns the nth Fibonacci number using the fast-doubling algorithm.
    Time complexity: O(log n * M(n)), where M(n) is the complexity of integer multiplication.
    Space complexity: O(n) to store the large integer.
    
    fib(0) = 0, fib(1) = 1, ...
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    
    # Fast doubling identities:
    # F_{2k} = F_k * (2 * F_{k+1} - F_k)
    # F_{2k+1} = F_{k+1}^2 + F_k^2

    a, b = 0, 1  # Represents (F_k, F_{k+1}) starting with k=0
    for bit in bin(n)[2:]:
        # Double the current index: k -> 2k
        c = a * (2 * b - a)
        d = a * a + b * b
        a, b = c, d
        
        if bit == '1':
            # If bit is 1, we want to move from (F_{2k}, F_{2k+1}) to (F_{2k+1}, F_{2k+2})
            # which is adding 1 to the index.
            a, b = b, a + b
            
    return a

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            start_time = time.time()
            result = fib(n)
            end_time = time.time()
            print(f"fib({n}) computed in {end_time - start_time:.4f} seconds.")
            # To avoid flooding stdout with huge numbers if n is very large:
            s_res = str(result)
            if len(s_res) > 50:
                print(f"Result (truncated): {s_res[:20]}...{s_res[-20:]}")
                print(f"Number of digits: {len(s_res)}")
            else:
                print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        # Quick test
        print(f"fib(0) = {fib(0)}")
        print(f"fib(1) = {fib(1)}")
        print(f"fib(2) = {fib(2)}")
        print(f"fib(3) = {fib(3)}")
        print(f"fib(10) = {fib(10)}")
        print(f"fib(100) = {fib(100)}")

