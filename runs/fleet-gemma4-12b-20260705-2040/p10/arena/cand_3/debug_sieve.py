def primes_up_to(n):
    if n < 2: return []
    if n == 2: return [2]
    if n == 3: return [2, 3]
    size = (n - 3) // 2 + 1
    is_prime = bytearray([1]) * size
    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        idx = (p - 3) // 2
        if is_prime[idx]:
            start = (p * p - 3) // 2
            num_to_mark = (size - 1 - start) // p + 1
            is_prime[start::p] = bytes([0]) * num_to_mark
    primes = [2]
    for i in range(size):
        if is_prime[i]:
            primes.append(2 * i + 3)
    return primes

n = 25
print(f"n={n}")
res = primes_up_to(n)
print(f"Result: {res}")
