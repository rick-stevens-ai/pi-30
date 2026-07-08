# Base conversion utilities supporting bases 2 through 36.
# to_base converts an integer (including negatives) to a lowercase string representation in the given base.
# parse_int converts such a string back to an integer, handling an optional leading '-'.

def to_base(n, base):
    """Convert integer *n* to a lowercase string in the given *base* (2‑36).

    Handles zero and negative numbers. Digits 0‑9 are represented as '0'‑'9' and
    values 10‑35 as 'a'‑'z'.
    """
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    digits = []
    while n:
        n, rem = divmod(n, base)
        if rem < 10:
            digits.append(chr(ord('0') + rem))
        else:
            digits.append(chr(ord('a') + rem - 10))
    return sign + "".join(reversed(digits))

def parse_int(s, base):
    """Parse a lowercase base-*base* string *s* (optionally prefixed with '-') into an int.

    The function mirrors Python's built‑in ``int(s, base)`` but explicitly supports
    the lowercase digit set required by the test suite.
    """
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36")
    return int(s, base)

