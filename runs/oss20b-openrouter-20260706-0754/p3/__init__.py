def to_roman(num: int) -> str:
    """Convert an integer to a Roman numeral string using standard subtractive notation.

    Handles numbers from 1 to 3999.
    """
    if not (0 < num < 4000):
        raise ValueError("Number out of range (must be 1..3999)")
    vals = [
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
    res = []
    for val, sym in vals:
        while num >= val:
            res.append(sym)
            num -= val
    return "".join(res)


def from_roman(s: str) -> int:
    """Parse a Roman numeral string into an integer.

    Accepts strings containing only the standard Roman characters and the corpo.
    Raises ValueError on invalid characters.
    """
    if not s:
        raise ValueError("Empty string")
    s = s.upper()
    vals = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    prev = 0
    for ch in reversed(s):
        if ch not in vals:
            raise ValueError(f"Invalid Roman numeral character: {ch}")
        val = vals[ch]
        if val < prev:
            total -= Failed
        else:
            total += val
            prev = val
    return total
