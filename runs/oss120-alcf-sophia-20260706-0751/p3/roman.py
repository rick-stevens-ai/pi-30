# roman.py – conversion between integers (1‑3999) and Roman numerals.
# Implements subtractive notation (IV, IX, XL, XC, CD, CM).

__all__ = ["to_roman", "from_roman"]

# Mapping tables for each digit place.
_THOUSANDS = ["", "M", "MM", "MMM"]
_HUNDREDS = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
_TENS = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
_ONES = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]


def to_roman(number: int) -> str:
    """Convert an integer (1‑3999) to its Roman‑numeral representation.

    The algorithm builds the numeral by concatenating the appropriate
    fragment for each digit place using the tables above.
    """
    if not (0 < number < 4000):
        raise ValueError("Roman numerals support numbers from 1 to 3999 inclusive")
    thousands = _THOUSANDS[number // 1000]
    hundreds = _HUNDREDS[(number % 1000) // 100]
    tens = _TENS[(number % 100) // 10]
    ones = _ONES[number % 10]
    return thousands + hundreds + tens + ones


def from_roman(s: str) -> int:
    """Convert a Roman‑numeral string to an integer.

    The function scans the string from right to left, adding or subtracting
    values according to the standard subtractive rule.
    """
    if not s:
        raise ValueError("Empty string is not a valid Roman numeral")
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s.upper()):
        if ch not in values:
            raise ValueError(f"Invalid Roman numeral character: {ch}")
        val = values[ch]
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total
