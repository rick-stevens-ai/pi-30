def to_roman(n):
    if not (1 <= n <= 3999):
        raise ValueError("Input must be between 1 and 3999")
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = []
    for value, numeral in vals:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def from_roman(s):
    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        val = roman_values[ch]
        if val < prev:
            total -= val
        else:
            total += val
        prev = val
    return total
