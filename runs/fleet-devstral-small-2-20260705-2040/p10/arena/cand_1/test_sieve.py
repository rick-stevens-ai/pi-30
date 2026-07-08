from sieve import primes_up_to

# Test cases
test_cases = [
    (0, []),      # n < 2
    (1, []),      # n < 2
    (2, [2]),     # n == 2
    (3, [2, 3]),  # n == 3
    (10, [2, 3, 5, 7]),  # n == 10
    (20, [2, 3, 5, 7, 11, 13, 17, 19]),  # n == 20
    (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),  # n == 30
]

for n, expected in test_cases:
    result = primes_up_to(n)
    if result != expected:
        print(f"FAIL: primes_up_to({n}) = {result}, expected {expected}")
    else:
        print(f"PASS: primes_up_to({n}) = {result}")

# Test edge case: n=1
print(f"primes_up_to(1) = {primes_up_to(1)}")

# Test that all returned numbers are <= n
for n in [10, 20, 30, 100]:
    primes = primes_up_to(n)
    if any(p > n for p in primes):
        print(f"ERROR: primes_up_to({n}) contains number > {n}")
    else:
        print(f"OK: All primes <= {n}")
