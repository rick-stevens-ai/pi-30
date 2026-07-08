'''Convert integers to and from Roman numerals using standard subtractive notation.

Provides two public functions:
    to_roman(n): int -> str
    from_roman(s): str -> int

Both functions raise ValueError for out‑of‑range inputs or malformed numerals.
'''  

# Mapping of Roman numeral symbols to their integer values, ordered
# from largest to smallest, including the subtractive forms.
_ROMAN_PAIRS = [
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

# Reverse lookup for parsing.
_SYMBOL_TO_VALUE = {sym: val for val, sym in _ROMAN_PAIRS}

def to_roman(number: int) -> str:
    """Return the Roman numeral representation of *number*.

    Supports the conventional range 1‑3999 inclusive.  Values outside this
    range raise ``ValueError``.
    """
    if not isinstance(number, int):
        raise ValueError("Roman numerals can only represent integers")
    if not (0 < number < 4000):
        raise ValueError("Roman numeral range is 1..3999")

    result = []
    remainder = number
    for value, symbol in _ROMAN_PAIRS:
        count, remainder = divmod(remainder, value)
        if count:
            result.append(symbol * count)
        if remainder == 0:
            break
    return "".join(result)

def from_roman(s: str) -> int:
    """Convert a Roman numeral string *s* back to an integer.

    The function validates that the numeral uses proper subtractive notation
    and does not contain illegal repetitions.  Invalid inputs raise
    ``ValueError``.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("Input must be a non‑empty string")
    i = 0
    total = 0
    length = len(s)
    while i < length:
        # Try to match a two‑character subtractive symbol first.
        if i + 1 < length:
            two = s[i:i+2]
            if two in _ROMAN_PAIRS:
                # two-character symbols are only those in the mapping where
                # the string length is 2.
                # Since _ROMAN_PAIRS is a list of tuples we cannot directly
                # test membership; build a set of two‑char symbols.
                pass
        i += 1
    # Simpler approach: iterate over the ordered pairs and consume symbols.
    i = 0
    while i < length:
        matched = False
        for value, symbol in _ROMAN_PAIRS:
            if s.startswith(symbol, i):
                total += value
                i += len(symbol)
                matched = True
                break
        if not matched:
            raise ValueError(f"Invalid Roman numeral at position {i}: {s}")
    # Validate by re‑encoding to ensure canonical form.
    if to_roman(total) != s:
        raise ValueError("Non‑canonical Roman numeral representation")
    return total
