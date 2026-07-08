import sieve

def test_large():
    # compute primes up to 1000 using simple sieve for verification
    def simple_primes(n):
        sieve = [True] * (n+1)
        sieve[0:2] = [False, False]
        for p in range(2, int(n**0.5)+1):
            if sieve[p]:
                for multiple in range(p*p, n+1, p):
                    sieve[multiple] = False
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    expected = simple_primes(1000)
    got = sieve.primes_up_to(1000)
    assert got == expected, f"Mismatch at n=1000: got {len(got)} primes, expected {len(expected)}"
    print("Large test passed (n=1000)")

if __name__ == "__main__":
    test_large()