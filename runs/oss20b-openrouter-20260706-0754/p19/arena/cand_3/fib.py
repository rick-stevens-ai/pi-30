"""Fast Fibonacci computation using fast‑doubling.

The module exposes a single function :func:`fib` that returns the ``n``‑th
Fibonacci number for the standard 0‑based sequence
``fib(0) == 0, fib(1) == 1``.

The implementation follows the classic fast‑doubling recurrence::

    F(2k)   = F(k) * (2*F(k+1) - F(k))
    F(2k+1) = F(k)**2 + F(k+1)**2

Because every step halves ``k`` the algorithm runs in :math:`O(log n)`
time and uses only integer arithmetic – Python's arbitrary‑precision
integers guarantee exact results for any ``n`` that fits in memory.

Typical usage::

    >>> from fib import fib
    >>> fib(10)
    55

A :class:`ValueError` is raised for negative inputs.
"""

from __future__ import annotations

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the n‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index into the Fibonacci sequence.

    Returns
    -------
    int
        ``fib(n)``
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")

    def _pair(k: int) -> tuple[int, int]:
        """Return a tuple (F(k), F(k+1)).

        The function implements the fast‑doubling identities recursively.
        Each recursion reduces ``k`` by half, so depth is O(log k).
        """
        if k == 0:
            return 0, 1
        a, b = _pair(k >> 1)
        c = a * ((b << 1) - a)  # F(2k)
        d = a * a + b * b      # F(2k+1)
        return (c, d) if (k & 1) == 0 else (d, c + d)

    return _pair(n)[0]

*** End of file ***