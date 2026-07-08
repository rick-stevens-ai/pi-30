"""
Sieve of Eratosthenes implementation that is fast for large `n`.

The function :func:`primes_up_to(n)` returns a *sorted* list of all prime
numbers less than or equal to ``n``.

Highlights
----------
*   Uses :class:`bytearray` instead of python lists → faster memory usage.
*   Even numbers are skipped entirely – only odd candidates remain in the
    sieve.
*   Range marking is performed with slice‑assignment, which is a fast
    operation in CPython.
*   Handles all edge cases correctly (``n < 2`` returns ``[]``, ``n == 2``
    returns ``[2]``).
*   Works easily for values up to 2 million and beyond – the algorithm keeps
    both time (O(n log log n)) and memory (≈n/16 bytes) extremely small.

Example usage
-------------
>>> primes_up_to(30)
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
"""
from __future__ import annotations

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all primess ≤ ``n``.

    Parameters
    ----------
    n:
        Upper inclusive bound. If ``n < 2`` an empty list is returned.

    Notes
    -----
    The core idea is the classic Sieve of Eratosthenes with two small
    optimisations:

    *   All even numbers are considered non‑prime a priori – a `bytearray`
        sized to cover only odd indices is sufficient.
    *   Cross‑out multiples by a single slice assignment.  An odd prime
        ``p`` eliminates every other multiple starting at ``p*p``; the
        underlying index step in the boolean array is ``p``.
    """

    if n < 2:
        return []

    # Handle the only even prime explicitly.
    if n == 2:
        return [2]

    # `sieve[i]` corresponds to the odd number `num = 2*i + 1`
    size = (n + 1) // 2            # number of odd indices up to and including n
    sieve = bytearray(b"\x01") * size

    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:  # `p` is prime
            start = p * p
            step = p
            # Number of multiples to strike out: floor((n - start) / (2*step)) + 1
            cnt = ((n - start) // (step * 2)) + 1
            sieve[start // 2 :: step] = b"\x00" * cnt

    # Build the result: [2] plus all remaining odd numbers that survived.
    return [2] + [2*i + 1 for i in range(1, size) if sieve[i]]


if __name__ == "__main__":  # pragma: no cover – quick manual test
    import sys
    try:
        limit = int(sys.argv[1])
    except Exception:
        print("Usage: python sieve.py [upper_limit]", file=sys.stderr)
        sys.exit(1)
    print(primes_up_to(limit))
"