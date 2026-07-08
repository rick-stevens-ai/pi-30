def ref(n):
    if n < 3: return 0
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    i = 2
    while i*i < n:
        if sieve[i]:
            sieve[i*i:n:i] = bytearray(len(sieve[i*i:n:i]))
        i += 1
    return sum(sieve)

# Test the reference implementation
for n in [0, 1, 2, 3, 10, 100]:
    print(f'n={n}, ref(n)={ref(n)}')