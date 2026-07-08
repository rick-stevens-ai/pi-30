"""Roman numeral <-> int conversion with subtractive notation."""

_TABLE = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
    (1, "I"),
]


def to_roman(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError("value must be a positive integer")
    out = []
    for value, sym in _TABLE:
        while n >= value:
            out.append(sym)
            n -= value
    return "".join(out)


def from_roman(s):
    if not s or not isinstance(s, str):
        raise ValueError("input must be a non-empty string")
    result = 0
    i = 0
    for value, sym in _TABLE:
        while s.startswith(sym, i):
            result += value
            i += len(sym)
    if i != len(s) or result == 0:
        raise ValueError("invalid Roman numeral: %r" % s)
    return result
