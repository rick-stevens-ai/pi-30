def to_base(n, base):
    """Return string representation of integer n in given base (2-36), lowercase."""
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return '0'
    sign = ''
    if n < 0:
        sign = '-'
        n = -n
    digits = []
    while n > 0:
        remainder = n % base
        if remainder < 10:
            digits.append(str(remainder))
        else:
            digits.append(chr(ord('a') + remainder - 10))
        n //= base
    return sign + ''.join(reversed(digits))


def parse_int(s, base):
    """Parse string s in given base (2-36) and return integer.
    Matches int(s, base) behavior.
    """
    return int(s, base)