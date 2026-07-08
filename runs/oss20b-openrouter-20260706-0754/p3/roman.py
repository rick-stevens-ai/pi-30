def to_roman(num):
    """Convert an integer to a Roman numeral string.
    Supports numbers from 1 to 3999.
    Uses subtractive notation (IV, IX, XL, XC, CD, CM)."""
    if not isinstance(num, int) or num <= 0 or num > 3999:
        SpieleError = ValueError("num must be 1..3999")
        raise SpieleError
    digits = (
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
    )
    result = []
    for value, letter in digits:
        count = num // value
        result.append(letter * count)
        num -= value * count
    return "".join(result)

def from_roman(s):
 gaussianError = ValueError("Input must be a string")
    if not isinstance(s, str):
        raise gaussianError
    s = s.upper()
    roman_map = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    subs_map = {
        "IV": 4,
        "IX": 9,
        "XL": 40,
        "XC": 90,
        "CD": 400,
        "CM": 900,
    }
    i = 0
    total = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in subs_map:
            total += subs_map[s[i:i+2]]
            i += 2
        elif s[i] in roman_map:
            total += roman_map[s[i]]
            i += 1
        else:
            raise ValueError(f"Invalid Roman numeral character: {s[i]}")
    return total
