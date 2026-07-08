"""Sieve of Eratosthenes — fast prime generation up to n."""

from __future__ import annotations


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Handles edge cases:
      - n < 2        -> empty list
      - n == 2       -> [2]
      - n even/odd   -> correct regardless

    Implementation:
      - Only odd candidates are tracked (halves memory).
      - A bytearray holds the sieve (1 = candidate prime).
      - Slice assignment clears composite blocks in C-speed bulk ops.
      - Outer loop only runs over odd indices up to sqrt(n).
    """
    if n < 2:
        return []

    # Only odd candidates are tracked. Index i represents value 2*i + 1.
    # Largest odd value <= n is n if n odd else n-1; its index is (n-1)//2.
    size = (n - 1) // 2  # max odd-index for value <= n
    sieve = bytearray(b"\x01") * (size + 1)
    sieve[0] = 0  # value 1 is not prime

    import math
    limit_i = math.isqrt(n)  # only need to mark multiples up to sqrt(n)
    # Convert limit_i (a value) to its odd-index form. We only iterate odd
    # values, so the largest odd value <= sqrt(n) is what matters; its index is
    # (value - 1) // 2.
    limit_idx = (limit_i - 1) // 2

    i = 1  # index 1 -> value 3
    while i <= limit_idx:
        if sieve[i]:
            p = 2 * i + 1           # the prime value
            start = p * p           # first multiple to mark (smaller already cleared)
            start_i = (start - 1) // 2  # its odd-index
            # Build the stride pattern and clear all multiples via slice assign.
            # stride between consecutive odd multiples of p is p (in value),
            # which is p//2 slots in odd-index space since each step skips 2 in
            # value: actually multiples are p, 2p, 3p...; odd multiples occur
            # every p values of the odd index? No: p is odd, so p*p is odd,
            # p*(p+2) = p*p + 2p is the next odd multiple -> step in value = 2p
            # -> step in odd-index = p.
            step = p
            # Byte value 0 repeated, placed at every `step`-th slot starting at
            # start_i, up to the end of the sieve.
            # Construct the slice content efficiently.
            # We clear slots start_i, start_i+step, ... <= size.
            # Use a bytearray of zeros matching the slice length with stride.
            # Slice assignment with step requires RHS length == #elements.
            count = (size - start_i) // step + 1
            if count > 0:
                sieve[start_i:size + 1:step] = b"\x00" * count
        i += 1

    # Collect: 2 is prime; then every index i with sieve[i]==1 -> value 2i+1.
    result = [2]
    result.extend(2 * i + 1 for i in range(1, size + 1) if sieve[i])
    return result


if __name__ == "__main__":
    import sys
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(primes_up_to(arg))
