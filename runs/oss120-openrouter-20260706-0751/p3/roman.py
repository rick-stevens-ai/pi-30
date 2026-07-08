# roman.py - simple conversion using subtractive notation

_roman_numerals = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
]

def to_roman(num: int) -> str:
    """Convert an integer (1-3999) to a Roman numeral using subtractive notation."""
    if not (0 < num < 4000):
        raise ValueError('Number out of range (must be 1..3999)')
    result = []
    for value, numeral in _roman_numerals:
        while num >= value:
            result.append(numeral)
            num -= value
    return ''.join(result)

def from_roman(s: str) -> int:
    """Convert a Roman numeral string to an integer. Supports subtractive forms."""
    s = s.upper()
    i = 0
    total = 0
    numeral_map = {n: v for v, n in _roman_numerals}
    while i < len(s):
        # Look ahead two characters for subtractive pair
        if i + 1 < len(s) and s[i:i+2] in numeral_map:
            total += numeral_map[s[i:i+2]]
            i += 2
        else:
            total += numeral_map[s[i]]
            i += 1
    return total
