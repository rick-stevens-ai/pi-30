"""Fast Fibonacci implementation using the fast doubling method.

This module exposes a single function :func:`fib` that returns the
``n``\-th Fibonacci number using an :math:`\mathcal{O}(\log n)` algorithm.

It relies solely on the Python standard library and uses Python's
built‑in arbitrary precision integers.

```python
>>> from fib import fib
>>> fib(0)
0
>>> fib(1)
1
>>> fib(10)
55
>>> fib(200_000)
...  # very fast
```
"""

from __future__ import annotations

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the `n`\-th Fibonacci number.

    Parameters
    ----------
    n : int
        Non‑negative integer index of the Fibonacci number.

    Returns
    -------
    int
        The value of :math:`F(n)`.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be non‑negative, got {}".format(n))
    a, b = 0, 1  # a = F(k), b = F(k+1)
    for i in range(n.bit_length() - 1, -1, -1):
        c = a * ((b << 1) - a)          # F(2k)
        d = a * a + b * b               # F(2k + 1)
        if (n >> i) & 1:
            a, b = d, c + d
        else:
            a, b = c, d
    return a

*** End of Output ***