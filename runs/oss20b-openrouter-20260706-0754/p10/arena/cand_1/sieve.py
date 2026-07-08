"""Efficient Sieve of Eratosthenes implementation.

The :func:`primes_up_to` function returns a sorted list of all primes
less than or equal to ``n``.

The implementation is optimized for values up to at least 2 000 000 using
Python's :class:`bytearray` and slice assignment.

Only modules from the Python standard library are imported.
"""

from __future__ import annotations

__all__ = ["primes_up_to"]


+def _sieve_span(n: int) -> bytearray:
+    """Return a bytearray representing which odd numbers up to *n* are prime.
+
+    The array index ``i`` represents the odd number ``2*i + 1``.  Index
+    ``0`` (number 1) is a dummy placeholder and will be ignored.  The
+    value ``1`` means 'prime', ``0`` means 'composite'.
+    """
+
+    # Number of odd numbers from 1 to n inclusive.
+    size = (n - 1) // 2
+    sieve = bytearray(b"\x01") * (size + 1)  # index 0 is dummy
+
+    import math
+    limit = int(math.isqrt(n))
+    # Iterate over odd primes starting at 3.
+    for p in range(3, limit + 1, 2):
+        if sieve[p // 2]:  # prime flag
+            start = (p * p) // 2
+            step = p
+            sieve[start::step] = b"\x00" * (((len(sieve) - start - 1) // step) + 1)
+    return sieve
+
+
+def primes_up_to(n: int) -> list[int]:
+    """Return a sorted list of all primes ≤ ``n``.
+
+    Parameters
+    ----------
+    n : int
+        The inclusive upper bound for primes. ``n`` may be any integer;
+        values less than 2 return an empty list.
+    """
+
+    if n < 2:
+        return []
+
+    sieve = _sieve_span(n)
+    primes: list[int] = [2]
+    # ``enumerate`` gives index, flag; check flag for 1.
+    for idx, flag in enumerate(sieve[1:], start=1):  # skip dummy
+        if flag:
+            primes.append(2 * idx + 1)
+    return primes
+
+
+if __name__ == "__main__":
+    import sys
+
+    if len(sys.argv) < 2:
+        print("Usage: python sieve.py <upper_bound>")
+        sys.exit(1)
+    try:
+        upper = int(sys.argv[1])
+    except ValueError:
+        print("<upper_bound> must be an integer")
+        sys.exit()
+    print(primes_up_to(upper))
*** End of file ***