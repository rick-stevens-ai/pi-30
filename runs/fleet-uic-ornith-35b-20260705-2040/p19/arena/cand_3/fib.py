"""fast-doubling Fibonacci — iterative MSB-first traversal.

Build (F_k, F_{k+1}) one bit at a time working from the top of n downward:
    F_{2m} =       F_m · ( 2F_{m+1} − F_m )              even case
    F_{2m+1} =     F_m² + F_{m+1}²
    advance one more step if an MSB is set.

Pure Python, no recursion, no imports, O(log n) big-integer multiplications.
"""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1). O(|log_2 n|) muls."""

    if n < 2:
        return n                                  # F_0 = 0,   F_1 = 1

    hi = n.bit_length() - 1                       # index of MSB in binary form
    lo, hi_lo = 0, 1                              # (F_k, F_{k+1}) — k starts at 0

    for i in range(hi, -1, -1):                   # process each bit top → down
        h = lo * ((hi_lo << 1) - lo)              #   F_{2m} = F_m (2F_{m+1} − F_m)
        f = hi_lo * hi_lo + lo * lo               #   F_{2m+1} = F_m²     + F_{m+1}²
        if (n >> i) & 1:                          # MSB is set — advance one further
            lo, hi_lo = f, h + f                  # new pair at index 2m+1 == F_{2m+1}, F_{2m+2}=F_{2m}+F_{2m+1}
        else:                                     # bit zero — skip ahead → index 2m
            lo, hi_lo = h, f

    return lo
