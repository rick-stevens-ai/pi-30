def count_primes(n):
    if n < 2:
        return 0
    sieve = bytearray([1]) * ((n + 1) // 2)
    sieve[0] = 0
    for i in range(1, int(n**0.5) // 2 + 1):
        if sieve[i]:
            prime = 2 * i + 1
            start = prime * prime // 2
            sieve[start::prime] = b'\x00' * len(sieve[start::prime])
    return sum(sieve)

print('n=10:', count_primes(10))
print('Expected: 4')
print('Primes under 10: 2, 3, 5, 7')

# Debug the sieve
n = 10
sieve = bytearray([1]) * ((n + 1) // 2)
sieve[0] = 0
print('Initial sieve (odd numbers only):', list(sieve))
print('Indices represent: 1,3,5,7,9')

for i in range(1, int(n**0.5) // 2 + 1):
    print(f'Checking i={i}, sieve[{i}]={sieve[i]}')
    if sieve[i]:
        prime = 2 * i + 1
        start = prime * prime // 2
        print(f'  Prime={prime}, start={start}')
        sieve[start::prime] = b'\x00' * len(sieve[start::prime])
        print(f'  Sieve after marking multiples: {list(sieve)}')

print('Final count:', sum(sieve))