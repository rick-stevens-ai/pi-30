'''Roman numeral conversion utilities.

Provides `to_roman` and `from_roman` functions supporting the standard
subtractive notation (IV, IX, XL, XC, CD, CM) for numbers in the range
1‑3999 inclusive.
'''

from __future__ import annotations

# Mapping of integer values to Roman numeral symbols, ordered from highest to lowest.
_ROMAN_TABLE = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

# Reverse lookup for single‑character symbols used by the parser.
_SINGLE_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

def to_roman(n: int) -> str:
    """Convert an integer ``n`` (1 ≤ n < 4000) to a Roman numeral string.

    The implementation uses a greedy algorithm based on the ordered
    ``_ROMAN_TABLE`` which already contains the subtractive forms.
    """
    if not (0 < n < 4000):
        raise ValueError("Roman numerals support numbers from 1 to 3999 inclusive")
    result: list[str] = []
    for value, symbol in _ROMAN_TABLE:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)

def from_roman(s: str) -> int:
    """Convert a Roman numeral string ``s`` to its integer value.

    The parser walks the string left‑to‑right, handling subtractive pairs
    when a smaller‑valued symbol precedes a larger one.
    """
    i = 0
    total = 0
    while i < len(s):
        # Look ahead to detect a subtractive pair.
        if i + 1 < len(s) and _SINGLE_VALUES[s[i]] < _SINGLE_VALUES[s[i + 1]]:
            total += _SINGLE_VALUES[s[i + 1]] - _SINGLE_VALUES[s[i]]
            i += 2
        else:
            total += _SINGLE_VALUES[s[i]]
            i += 1
    return total

__all__ = ["to_roman", "from_roman"]
