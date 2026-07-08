DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'[:36]  # lowercase for base 2-36

def to_base(n, base):
    """Convert integer n to lowercase string in given base (2-36)."""
    if base < 2 or base > 36:
        raise ValueError(f"base must be 2-36, got {base}")
    if n == 0:
        return '0'
    negative = n < 0
    n = abs(n)
    result = []
    while n:
        result.append(DIGITS[n % base])
        n //= base
    if negative:
        result.append('-')
    return ''.join(reversed(result))

def parse_int(s, base):
    """Parse string s in given base (2-36) to integer. Handles negatives."""
    if base < 2 or base > 36:
        raise ValueError(f"base must be 2-36, got {base}")
    return int(s, base)
