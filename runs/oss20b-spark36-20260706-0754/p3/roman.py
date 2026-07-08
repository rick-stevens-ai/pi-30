"""
Roman numeral conversion utilities.

Provides two functions:
- :func:`to_roman(n)` returns the minimal Roman representation for an integer n in [1,3999].
- :func:`from_roman(s)` parses a Roman numeral string (uppercase) and returns its integer value.

The implementation uses the standard subtractive notation: IV, IX, XL, XC, CD, CM.
"""

# Mapping of values to numerals in descending order.
_RANGES = [
    (1000, "M"),
    (900,  "CM"),
    (500,  "D"),
    (400,  "CD"),
    (100,  "C"),
    (90,   "XC"),
    (50,   "L"),
    (40,   "XL"),
    (10,   "X"),
    (9,    "IX"),
    (5,    "V"),
    (4,    "IV"),
    (1,    "I"),
]

# Helper for quick value lookup when parsing.
_VAL_MAP = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}


def to_roman(n: int) -> str:
    """Convert an integer ``n`` (1 <= n <= 3999) to a Roman numeral.

    Raises :class:`ValueError` if the number is outside the valid range.
    """
    if not isinstance(n, int):
        raise TypeError("to_roman requires an integer argument")
    if n < 1 or n > 3999:
        raise ValueError("integer out of range (must be 1..3999)")
    result = []
    for value, numeral in _RANGES:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def from_roman(s: str) -> int:
    """Parse a Roman numeral string ``s`` and return its integer value.

    The function is case-insensitive but expects the standard subtractive notation.
    Raises :class:`ValueError` for invalid strings or empty input.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("from_roman requires a non-empty string")
    s = s.upper()
    i = 0
    total = 0
    while i < len(s):
        # Check for two-character subtractive pattern first.
        if i + 1 < len(s) and s[i:i+2] in {"IV", "IX", "XL", "XC", "CD", "CM"}:
            total += {
                "IV":4, "IX":9,
                "XL":40, "XC":90,
                "CD":400, "CM":900
            }[s[i:i+2]]
            i += 2
        else:
            ch = s[i]
            if ch not in _VAL_MAP:
                raise ValueError(f"invalid Roman numeral character: {ch}")
            total += _VAL_MAP[ch]
            i += 1
    return total

__all__ = ["to_roman", "from_roman"]
