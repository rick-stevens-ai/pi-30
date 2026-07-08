def count_primes(n):
    if n < 3:
        return 0
    sieve = bytearray([1]) * ((n + 1) // 2)
    sieve[0] = 0
    for i in range(1, int(n**0.5) // 2 + 1):
        if sieve[i]:
            prime = 2 * i + 1
            start = prime * prime // 2
            sieve[start::prime] = b'\x00' * len(sieve[start::prime])
    return 1 + sum(sieve)

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

print('Testing n=3:')
print('My function:', count_primes(3))
print('Reference:', ref(3))
print('Expected: 1 (only prime < 3 is 2)')

# Debug my function
n = 3
print(f'\nDebugging n={n}:')
print(f'sieve size: {(n + 1) // 2}')
sieve = bytearray([1]) * ((n + 1) // 2)
print(f'Initial sieve: {list(sieve)}')
print(f'Sieve indices represent odd numbers: 1, 3')
sieve[0] = 0
print(f'After marking 1 as non-prime: {list(sieve)}')

print(f'int(n**0.5) // 2 = {int(n**0.5) // 2}')
for i in range(1, int(n**0.5) // 2 + 1):
    print(f'Checking i={i}, sieve[{i}]={sieve[i]}')
    if sieve[i]:
        prime = 2 * i + 1
        start = prime * prime // 2
        print(f'  Prime={prime}, start={start}')
        sieve[start::prime] = b'\x00' * len(sieve[start::prime])
        print(f'  Sieve after marking: {list(sieve)}')

print(f'Final sum(sieve) = {sum(sieve)}')
print(f'1 + sum(sieve) = {1 + sum(sieve)}')