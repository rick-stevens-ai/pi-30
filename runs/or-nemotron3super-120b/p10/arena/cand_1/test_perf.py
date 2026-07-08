import time
import sieve

n = 2_000_000
start = time.perf_counter()
primes = sieve.primes_up_to(n)
elapsed = time.perf_counter() - start
print(f"primes_up_to({n}) took {elapsed:.4f} seconds")
print(f"Number of primes found: {len(primes)}")
# Quick sanity: check that number of primes approx n / ln(n)
import math
expected = n / math.log(n)
print(f"Expected ~{expected:.0f} primes")
assert abs(len(primes) - expected) < 0.1 * expected  # within 10%