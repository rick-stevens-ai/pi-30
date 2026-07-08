# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    def is_prime(x):
        if x < 2: return False
        i = 2
        while i * i <= x:
            if x % i == 0:
                return False
            i += 1
        return True
    return sum(1 for x in range(n) if is_prime(x))
