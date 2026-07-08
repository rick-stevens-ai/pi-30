"""Fast Fibonacci computation using the fast‑doubling algorithm.

The :func:`fib` function calculates the *n*th Fibonacci number with exact
bigint arithmetic (Python's arbitrary‑precision integers) and a time
complexity of :math:`O(log n)`.

Note
----
* ``fib(0)`` returns ``0`` and ``fib(1)`` returns ``1``.
* The implementation is deliberately simple and uses only built‑in
  operations.

Example
-------
>>> fib(0)
0
>>> fib(1)
1
>>> fib(10)
55
 competitie
>>> fib(100)
354224848179261915075
"""

from __future__ import annotations

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative integer index of the Fibonacci sequence.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    # Fast doubling iteration: start with F(0)=0, F(1)=1.
    a, b = 0, 1
    # Process bits of n from most significant to least significant.
    for i in reversed(range(n.bit_length())):
        # Compute F(2k) and F(2k+1) from F(k)=a, F(k+1)=b.
        c = a * ((b << 1) - a)
        d = a * a + b * b
        # If the current bit is 1, shift to the odd index.
        if (n >> i) & 1:
            a, b = d, c + d
        else:
            a, b = c, d
    return a


if __name__ == "__main__":
    import sys
    try:
        n = int(sys.argv[1])
    except Exception as exc:
        sys.exit("Usage: fib.py <non‑negative integer>\nError: " + str(exc))
    print(fib(n))
