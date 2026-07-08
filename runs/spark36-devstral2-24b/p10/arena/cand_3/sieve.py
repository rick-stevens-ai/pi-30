"""
Generate primes up to n using the Sieve of Eratosthenes.

Exposes:
    primes_up_to(n) -> sorted list of primes <= n
    - Correct for n<2 (empty)
    - Fast for large n (bytearray, skip even numbers)
    - Stdlib only (no dependencies)
"""

def primes_up_to(n: int) -> list[int]:
    """Return all prime numbers <= n."""
    if n < 2:
        return []

    # Use bytearray to save memory vs list[bool]
    # Store only odd candidates >=3, so size is roughly n/2
    max_odd = n if n % 2 == 1 else n - 1
    size = (max_odd - 1) // 2  # Index 0 represents 3, index k represents 3+2*k
    if size <= 0:
        return [2] if n >= 2 else []

    sieve = bytearray([True]) * size

    # Square root of the maximum odd number represented: sqrt(3+2*(size-1)) = sqrt(n)
    limit = int(max_odd ** 0.5) // 2

    # Mark multiples starting from 3 on
    for k in range(size):
        if not sieve[k]:
            continue
        num = 3 + 2 * k
        # Start marking from the first odd multiple: num*num
        start = (num * num - 1) // 2  # index for num^2
        step = num  # alternate odd/even, but in our scheme steps by num in odd rep

        if num > limit:
            break

        # Efficient range assignment using slices
        sieve[start::step] = b'\x00' * len(sieve[start::step])

    primes: list[int] = []
    if n >= 2:
        primes.append(2)
    primes.extend(3 + 2 * k for k, is_prime in enumerate(sieve) if is_prime and (3 + 2 * k <= n))

    return primes
