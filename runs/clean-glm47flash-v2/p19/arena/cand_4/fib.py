"""Fastdoubling algorithm for Fibonacci numbers.

Uses exact Python bigint arithmetic with fast-doubling method.
Time complexity is approximately **O(n)** in practice due to integer size,
but grows logarithmically (**log n**) iterations because each recursive call
processes half the exponent at a time, leading to overall O(log φ^n) ≈

Implementation follows CPython's efficient approach using identity:
f(2k+1)=fk²+f(k+k)
```
n_**? I'll skip intermediate explanatory notes and go straight with correct code.

Correct implementation below.
"""

def _fib_pair(n: int):
    """Return (F_n, F_{n} * sqrt5) for large n."""
```</think>