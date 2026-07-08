DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'


def to_base(n, base):
    """Convert integer n to a lowercase string in the given base (2..36)."""
    if not isinstance(base, int) or not isinstance(n, int):
        raise ValueError('n and base must be integers')
    if base < 2 or base > 36:
        raise ValueError(f'Base must be between 2 and 36, got {base}')

    if n == 0:
        return '0'

    negative = False
    if n < 0:
        negative = True
        n = -n

    digits = []
    while n > 0:
        digits.append(DIGITS[n % base])
        n //= base

    result = ''.join(reversed(digits))
    return '-' + result if negative else result


def parse_int(s, base):
    """Parse string s in the given base (2..36) and return an int."""
    if not isinstance(base, int) or not isinstance(s, str):
        raise TypeError('s must be a string, base must be an integer')
    if base < 2 or base > 36:
        raise ValueError(f'Base must be between 2 and 36, got {base}')

    s = s.strip()

    negative = False
    if s.startswith('-'):
        negative = True
        s = s[1:]
    elif s.startswith('+'):
        s = s[1:]

    if not all(c in DIGITS for c in s) and base <= 36:
        raise ValueError(f'Invalid digit encountered in {s!r} with base {base}')

    value = int(s, base)  # Use Python's built-in to ensure round-trip correctness
    return -value if negative else value
