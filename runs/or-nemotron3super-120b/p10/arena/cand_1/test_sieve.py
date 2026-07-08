import sieve

def simple_sieve(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            for multiple in range(p*p, n+1, p):
                sieve[multiple] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def test():
    max_n = 2000
    errors = []
    for n in range(max_n + 1):
        a = sieve.primes_up_to(n)
        b = simple_sieve(n)
        if a != b:
            errors.append((n, a, b))
    if errors:
        print("Found errors:")
        for n, a, b in errors[:10]:
            print(f"n={n}: got {a}, expected {b}")
        return False
    else:
        print(f"All tests passed up to n={max_n}")
        return True

if __name__ == "__main__":
    test()