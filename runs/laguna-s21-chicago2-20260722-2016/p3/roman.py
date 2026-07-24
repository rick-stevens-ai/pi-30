"""Roman numeral conversion with subtractive notation."""

# Ordered from largest to smallest value, including subtractive pairs.
_NUMERALS = [
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


def to_roman(n):
    if not 1 <= n <= 3999:
        raise ValueError("Roman numerals only support 1..3999")
    result = []
    for value, numeral in _NUMERALS:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def from_roman(s):
    values = {"I": 1, "V": 5, "X": 10, "L": 50,
              "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        cur = values[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
        prev = cur
    return total