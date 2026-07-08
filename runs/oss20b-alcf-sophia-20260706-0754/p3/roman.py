"""Roman numeral conversion utilities.

Provides :func:`to_roman` which converts a positive integer to a Roman numeral
string using standard subtractive notation, and :func:`from_roman` which parses
a Roman numeral back to an integer.  The implementation is intentionally
compact and easy to read, focusing on correctness for the range 1‑3999 which
is what the tests exercise.

The module does not depend on any external libraries and is safe to import
even when a third‑party ``roman`` pip package is present, because the file
resides in the current directory and shadows the pip package during imports.
"""

# Mapping of integer values to Roman numerals, sorted from largest to
# smallest. Including the subtractive pairs ensures the algorithm uses the
# preferred notation.
_ROMAN_MAP = [
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

# Reverse mapping from symbol to value for parsing.
_ROMAN_VALUE = {sym: val for val, sym in _ROMAN_MAP}

# Navigable mapping of single-character symbols to values.
_ROMAN_CHAR_VALUE = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def to_roman(n: int) -> str:
    """Return the Roman numeral representation of ``n``.

    Parameters
    ----------
    n: int
        Positive integer (1 ≤ n ≤ 3999).  Values outside this range raise
        :class:`ValueError`.

    Returns
    -------
    str
        Roman numeral string.
    """
    if not isinstance(n, int) or n < 1 or n > 3999:
        raise ValueError("Roman numerals are defined for 1 ≤ n ≤ 3999")

    result = []
    for value, symbol in _ROMAN_MAP:
        while n >= value:
            n -= value
            result.append(symbol)
    return "".join(result)


def from_roman(s: str) -> int:
    """Parse a Roman numeral string ``s`` into an integer.

    The function supports standard subtractive notation (e.g. ``IV`` for 4)
    and is strict: it raises :class:`ValueError` if the string contains
    characters that are not valid Roman numerals or if the string does not
    represent a number in the canonical form.

    Parameters
    ----------
    s: str
        Roman numeral string.

    Returns
    -------
    int
        Integer representation.
    """
    if not s:
        raise ValueError("Empty string is not a valid Roman numeral")

    total = 0
    i = 0
    length = len(s)
    while i < length:
        ch = s[i]
        if ch not in _ROMAN_CHAR_VALUE:
            raise ValueError(f"Invalid Roman numeral character: {ch}")
        val = _ROMAN_CHAR_VALUE[ch]
        # Look ahead for possible subtractive pattern.
        if i + 1 < length:
            next_ch = s[i + 1]
            if next_ch not in _ROMAN_CHAR_VALUE:
                raise ValueError(f"Invalid Roman numeral character: {next_ch}")
            next_val = _ROMAN_CHAR_VALUE[next_ch]
            if val < next_val:
                # Subtractive pair.
                total += next_val - val
                i += 2
                continue
        total += val
        i += 1
    # Validate round‑trip: convert back to ensure canonical form.
    if to_roman(total) != s:
        raise ValueError("Non‑canonical or malformed Roman numeral")
    return total

__all__ = ["to_roman", "from_roman"]
