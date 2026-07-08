"""Roman numeral conversion functions."""

# Roman numeral values in descending order
ROMAN_NUMERALS = [
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


def to_roman(n: int) -> str:
    """Convert an integer to a Roman numeral."""
    if not isinstance(n, int):
        raise TypeError("Expected integer")
    if n <= 0 or n >= 4000:
        raise ValueError("Argument must be between 1 and 3999")
    
    result = []
    for value, numeral in ROMAN_NUMERALS:
        count, n = divmod(n, value)
        result.append(numeral * count)
        if n == 0:
            break
    return "".join(result)


def from_roman(s: str) -> int:
    """Convert a Roman numeral to an integer."""
    if not isinstance(s, str):
        raise TypeError("Expected string")
    if not s:
        raise ValueError("Empty string")
    
    result = 0
    i = 0
    s = s.upper()
    
    for value, numeral in ROMAN_NUMERALS:
        while s.startswith(numeral, i):
            result += value
            i += len(numeral)
    
    if i != len(s):
        raise ValueError("Invalid Roman numeral")
    
    return result
