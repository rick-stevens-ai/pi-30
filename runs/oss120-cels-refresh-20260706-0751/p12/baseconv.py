# Implement base conversion for bases 2..36 with lowercase digits.
# to_base: integer n -> string representation in given base (lowercase), handling 0 and negatives.
# parse_int: string s (lowercase digits, optional leading '-') -> integer value in given base.

def _digit_char(val):
    """Return character for digit value 0-35."""
    if 0 <= val <= 9:
        return chr(ord('0') + val)
    elif 10 <= val < 36:
        return chr(ord('a') + (val - 10))
    else:
        raise ValueError('Invalid digit value')

def _char_value(ch):
    """Return numeric value of a digit character (0-9, a-z)."""
    if '0' <= ch <= '9':
        return ord(ch) - ord('0')
    if 'a' <= ch <= 'z':
        return ord(ch) - ord('a') + 10
    raise ValueError(f'Invalid digit character: {ch}')

def to_base(n, base):
    if not (2 <= base <= 36):
        raise ValueError('base must be between 2 and 36')
    if n == 0:
        return '0'
    sign = '-' if n < 0 else ''
    n = abs(n)
    digits = []
    while n:
        n, rem = divmod(n, base)
        digits.append(_digit_char(rem))
    return sign + ''.join(reversed(digits))

def parse_int(s, base):
    if not (2 <= base <= 36):
        raise ValueError('base must be between 2 and 36')
    if not s:
        raise ValueError('empty string')
    sign = -1 if s[0] == '-' else 1
    if s[0] in '+-':
        s = s[1:]
    if not s:
        raise ValueError('no digits')
    value = 0
    for ch in s:
        val = _char_value(ch)
        if val >= base:
            raise ValueError(f'digit {ch} out of range for base {base}')
        value = value * base + val
    return sign * value
