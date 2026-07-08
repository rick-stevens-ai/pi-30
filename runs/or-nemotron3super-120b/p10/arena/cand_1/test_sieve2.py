import sys
sys.path.insert(0, '.')
from sieve import primes_up_to
import random, math

def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True

def test(n):
    got = primes_up_to(n)
    expected = [i for i in range(2, n+1) if is_prime(i)]
    if got != expected:
        print(f"FAIL n={n}: got {got}, expected {expected}")
        return False
    return True

# systematic small range
for n in range(0, 500):
    if not test(n):
        break
else:
    print("Small range OK")

# random larger numbers
random.seed(42)
for _ in range(100):
    n = random.randint(500, 5000)
    if not test(n):
        break
else:
    print("Random up to 5000 OK")

# edge cases: powers of two, squares
for n in [2**i for i in range(0, 13)]:
    test(n)
print("Powers of two OK")
for n in [i*i for i in range(1, 50)]:
    test(n)
print("Squares OK")
print("All tests passed")
