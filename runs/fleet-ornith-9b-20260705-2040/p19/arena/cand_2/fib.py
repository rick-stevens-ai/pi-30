def fib(n):
    """Return the nth Fibonacci number F(n) using fast doubling, O(log n).

    F(0)=0, F(1)=1.  Uses Python's arbitrary-precision integers for exact
    results at any n (e.g. n=200000 produces a ~42000-digit number).
    """
    if n == 0:
        return 0

    # Fast-doubling recurrence:
    #   F(2k)   = F(k) * [2*F(k+1) - F(k)]
    #   F(2k+1) = F(k)^2 + F(k+1)^2
    # Iterate over all bits of n from MSB to LSB, maintaining (a,b)=(F(k),F(k+1)).

    a, b = 0, 1
    for bit in bin(n)[2:]:                 # every bit MSB→LSB
        c = a * ((b << 1) - a)            # F(2k)
        d = a * a + b * b                 # F(2k+1)
        if bit == '0':
            a, b = c, d                   # k → 2k
        else:
            a, b = d, c + d               # k → 2k+1

    return a


if __name__ == "__main__":
    import time
    t = time.perf_counter()
    print(f"F(200000) has {len(str(fib(200000)))} digits")
    print(f"elapsed: {time.perf_counter() - t:.4f}s")
