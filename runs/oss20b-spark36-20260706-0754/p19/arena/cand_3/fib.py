"""
Fast Fibonacci implementation using fast doubling.

The function :func:`fib` returns the *n*th Fibonacci number (with
``fib(0)==0`` and ``fib(1)==1``).  It uses a depth‑first recursion that
computes both F\(k\) and F\(k+1\) simultaneously, which gives an overall
time complexity of :math:`O(log n)` and keeps memory usage constant.

The implementation relies only on the Python standard library and takes
advantage of Python's arbitrary‑precision integers (`bigint`), so it can
handle very large results (e.g. ``fib(200000)`` ) in a fraction of a
second.
"""

from __future__ import annotations

__all__ = ["fib"]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return the pair `(F(n), F(n+1))` using fast doubling.

    The algorithm follows these identities for *k* = floor(n/2):

    .. math::
        \begin{aligned}
            F(2k)   &= F(k)\, [ 2\,F(k+1) - F(k) ]\\
            F(2k+1) &= F(k)^2 + F(k+1)^2
        \end{aligned}

    Recursion terminates at ``n == 0`` where the pair is simply
    ``(0, 1)``.
    """
    if n == 0:
        return (0, 1)

    k = n >> 1  # floor division by a power of two
    a, b = _fib_pair(k)          # F(k), F(k+1)
    c = a * ((b << 1) - a)       # a*(2*b - a)   ->  F(2k)
    d = a*a + b*b                # a^2 + b^2     ->  F(2k+1)

    if n & 1:  # n is odd -> return (F(2k+1), F(2k) + F(2k+1))
        return d, c + d
    else:
        return c, d


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative integer index.  ``fib(0)`` is ``0`` and
        ``fib(1)`` is ``1``.

    Returns
    -------
    int
        The value of F\(n\).

    Raises
    ------
    ValueError
        If *n* is negative.

    Notes
    -----
    The function runs in :math:`O(log n)` time and uses only a few bytes
    of constant extra memory, making it fast even for very large values
    such as ``n = 200000``.
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    import sys
    try:
        idx = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError as exc:  # pragma: no cover - user error handling
        print("Usage: python fib.py [index]", file=sys.stderr)
        raise SystemExit(2) from exc

    print(f"fib({idx}) = {fib(idx)}")
