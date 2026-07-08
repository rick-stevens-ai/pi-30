# fib.py
"""Fast Fibonacci using the fast‑doubling method.

Provides a single public function ``fib(n)`` that returns the *n*‑th
Fibonacci number with ``fib(0) == 0`` and ``fib(1) == 1``.

The implementation is pure Python, relies only on the standard library and
uses the fast‑doubling recurrence which computes ``F(k)`` and ``F(k+1)``
from ``F(⌊k/2⌋)`` and ``F(⌊k/2⌋+1)`` in O(log n) time.  Because Python's ``int``
type has arbitrary precision, the function returns an exact bigint for any
non‑negative integer ``n`` – it comfortably handles values like ``n = 200_000``
in a few milliseconds.

The algorithm is implemented recursively but the recursion depth is at most
``log2(n)`` (≈ 18 for ``n = 200_000``), so it is safe for the typical Python
recursion limit.
"""

from __future__ import annotations

__all__ = ["fib"]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return ``(F(n), F(n + 1))`` using fast‑doubling.

    The function works for *n* ≥ 0.  It is a thin recursive wrapper around the
    classic identities:

    * ``F(2k)   = F(k) * (2*F(k+1) – F(k))``
    * ``F(2k+1) = F(k+1)**2 + F(k)**2``

    The recursion stops at ``n == 0`` where ``(F(0), F(1)) == (0, 1)``.
    """
    if n == 0:
        return 0, 1
    # Recursively compute (F(k), F(k+1)) where k = n // 2
    a, b = _fib_pair(n >> 1)
    # Apply doubling formulas
    c = a * ((b << 1) - a)   # F(2k)
    d = a * a + b * b        # F(2k+1)
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return d, c + d
    else:
        # n is even -> return (F(2k), F(2k+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the Fibonacci sequence.

    Returns
    -------
    int
        ``F(n)`` where ``F(0) == 0`` and ``F(1) == 1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    # ``_fib_pair`` already returns ``F(n)`` as the first element.
    return _fib_pair(n)[0]

# ---------------------------------------------------------------------------
# Simple sanity‑check when run as a script.  This is *not* part of the public
# API but provides a quick way to verify correctness during development.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    try:
        arg = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        print("Usage: python fib.py [non‑negative integer]")
        sys.exit(1)
    print(fib(arg))
