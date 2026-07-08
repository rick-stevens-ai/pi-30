"""
Fast Fibonacci computation using the fast‑doubling method.

The function ``fib`` returns the *exact* integer value of the nth Fibonacci number
(F_0 = 0, F_1 = 1) using only the Python standard library. The algorithm has a
time complexity of O(log n), which allows computing huge indices (e.g. n=200000)
in a few milliseconds.
"""
from __future__ import annotations

__all__: list[str] = ["fib"]


def fib(n: int) -> int:
    """Return the *exact* integer value of the nth Fibonacci number.

    Parameters
    ----------
    n : int
        Non‑negative index of the desired Fibonacci number. ``fib(0)`` returns
        0, ``fib(1)`` returns 1, etc.

    Returns
    -------
    int
        The nth Fibonacci number as a Python integer (arbitrary precision).

    Raises
    ------
    ValueError
        If ``n`` is negative.

    Notes
    -----
    The implementation uses the fast‑doubling recurrence:

    .. math::
        \begin{aligned}
            F_{2k}   &= F_k\, [2F_{k+1} - F_k],\\
            F_{2k+1} &= F_{k+1}^2 + F_k^2.
        
    The function ``_fib_pair`` returns the pair ``(F_n, F_{n+1})``.
    """

    if n < 0:
        raise ValueError("n must be non‑negative")

    def _fib_pair(k: int) -> tuple[int, int]:
        """Return the pair (F_k, F_{k+1}) using fast doubling.

        This helper is defined inside ``fib`` to avoid leaking into the module
        namespace while keeping the recursion depth negligible (log₂(n)).
        """
        if k == 0:
            return 0, 1
        # Recursive call for floor(k/2)
        a, b = _fib_pair(k >> 1)  # a=F_{k//2}, b=F_{k//2+1}
        c = a * ((b << 1) - a)    # F_{2m}   where m=k//2
        d = a * a + b * b          # F_{2m+1}
        if k & 1:
            # Odd index: return (d, c+d)
            return d, c + d
        else:
            # Even index: return (c, d)
            return c, d

    return _fib_pair(n)[0]

# Simple sanity check if run as a script.
if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        try:
            n = int(arg)
        except ValueError:
            print(f"{arg!r} is not an integer")
            continue
        try:
            print(f"fib({n}) = {fib(n)}")
        except Exception as exc:
            print(f"Error computing fib({n}): {exc}")
"