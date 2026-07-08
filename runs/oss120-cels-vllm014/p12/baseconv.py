# Base conversion utilities supporting bases 2..36.
# to_base(n, base) -> lowercase string representation of integer n in the given base.
# parse_int(s, base) -> integer parsed from string s in the given base.
# Both functions handle 0 and negative numbers, using lowercase digits 0-9 and a-z.

def _digit_char(value: int) -> str:
    """Return the character representation for a digit value (0 <= value < 36)."""
    if 0 <= value <= 9:
        return chr(ord('0') + value)
    else:
        return chr(ord('a') + (value - 10))


def to_base(n: int, base: int) -> str:
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36")
    # Handle zero explicitly
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n_abs = -n if n < 0 else n
    digits = []
    while n_abs > 0:
        n_abs, rem = divmod(n_abs, base)
        digits.append(_digit_char(rem))
    # digits are in reverse order
    return sign + ''.join(reversed(digits))


def _char_value(ch: str) -> int:
    """Return numeric value of a single digit character.
    Accepts '0'-'9', 'a'-'z', and also uppercase 'A'-'Z' for convenience.
    """
    if '0' <= ch <= '9':
        return ord(ch) - ord('0')
    if 'a' <= ch <= 'z':
        return 10 + ord(ch) - ord('a')
    if 'A' <= ch <= 'Z':
        return 10 + ord(ch) - ord('A')
    raise ValueError(f"invalid digit character: {ch}")


def parse_int(s: str, base: int) -> int:
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36")
    if not s:
        raise ValueError("empty string")
    sign = -1 if s[0] == '-' else 1
    start = 1 if s[0] in '+-' else 0
    value = 0
    for ch in s[start:]:
        digit = _char_value(ch)
        if digit >= base:
            raise ValueError(f"digit '{ch}' out of range for base {base}")
        value = value * base + digit
    return sign * value

