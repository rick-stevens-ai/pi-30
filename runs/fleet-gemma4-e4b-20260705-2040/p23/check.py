# P23 measurement-in-loop: count primes below N fast. correctness vs reference;
# signal = throughput. Seed is trial-division per number (O(n*sqrt n)). Target:
# 8.0 (Mn/s metric defined in bench). Loop should switch to a sieve.
from primecount import count_primes

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

def main():
    for n in (0, 1, 2, 3, 10, 100, 1000, 10000):
        if count_primes(n) != ref(n):
            print(f"WRONG n={n} got={count_primes(n)} exp={ref(n)}")
            raise SystemExit(1)
    print("OK correct")

if __name__ == "__main__":
    main()
