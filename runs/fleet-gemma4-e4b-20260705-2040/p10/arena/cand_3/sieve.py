import math

def primes_up_to(n: int) -> list[int]:
    """
    Computes all prime numbers less than or equal to n using a highly optimized 
    Sieve of Eratosthenes implementation.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A sorted list of primes up to n.
    """
    if n < 2:
        return []

    # Use bytearray for memory efficiency. Size is n + 1 to include index n.
    is_prime = bytearray([1] * (n + 1))
    
    # Mark 0 and 1 as not prime
    is_prime[0] = 0
    is_prime[1] = 0

    # Optimization: Skip all even numbers greater than 2.
    # This sets indices 4, 6, 8, ... to 0 in one go (slice assignment).
    if n >= 4:
        is_prime[4::2] = 0
    
    limit = int(math.sqrt(n)) + 1

    # Start sieving from p=3 (since evens are already handled)
    for p in range(3, limit, 2):
        # Check if p is marked as prime (only odd numbers are checked here)
        if is_prime[p] == 1:
            # Mark all multiples of p starting from p*p.
            # Since p is odd, p*p is also odd, so we start marking at an odd multiple.
            # We only need to mark odd multiples (p*p, p*p + 2p, p*p + 4p, ...) 
            # because even multiples are already marked as non-prime.
            
            start = p * p
            if start > n:
                break

            # We iterate over the odd multiples: i = start, start + 2*p, ..., <= n
            for i in range(start, n + 1, 2 * p):
                 is_prime[i] = 0

    # Collect all primes (indices where value is 1)
    primes = []
    # We only need to check odd numbers >= 3 and 2 itself.
    primes.append(2) # Handle the special case of 2
    for i in range(3, n + 1, 2):
        if is_prime[i] == 1:
            primes.append(i)

    return primes

# Example usage and testing for demonstration/verification
if __name__ == '__main__':
    print("--- Testing small cases ---")
    print(f"Primes up to 10: {primes_up_to(10)}") # Expected: [2, 3, 5, 7]
    print(f"Primes up to 1: {primes_up_to(1)}")   # Expected: []
    print(f"Primes up to 2: {primes_up_to(2)}")   # Expected: [2]

    N_test = 2000000
    import time
    start_time = time.time()
    result = primes_up_to(N_test)
    end_time = time.time()
    print(f"\n--- Testing large case (N={N_test}) ---")
    print(f"Found {len(result)} primes up to {N_test}.")
    print(f"Execution time: {end_time - start_time:.4f} seconds.")

    # Verify the last few primes are correct
    if result:
        print(f"Last 5 primes found: {result[-5:]}") # Should end with ..., 1999987, 1999993

