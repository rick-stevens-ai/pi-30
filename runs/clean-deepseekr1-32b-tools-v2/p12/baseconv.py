# P12 SEED: only base 10. to_base ignores base; parse_int uses int(s) base-10.
def to_base(n, base):
    if base < 2 or base > 36:
        raise ValueError('Base must be between 2 and 36')
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = []
    negate = False
    if n == 0:
        return '0'
    elif n < 0:
        negate = True
        n = -n
    while n > 0:
        remainder = n % base
        result.append(digits[remainder])
        n = n // base
    if negate:
        return '-' + ''.join(reversed(result))
    else:
        return ''.join(reversed(result))

def parse_int(s, base):
    s = s.strip().lower()
    if not isalnum(s):
        raise ValueError('Invalid character in string')
    negate = False
    if s.startswith('-'):
        return -parse_int(s[1:], base)
    total = 0
    for c in s.lower():
        value = '0123456789abcdefghijklmnopqrstuvwxyz'.find(c)
        if value == -1 or value >= base:
            raise ValueError('Invalid character for this base')
        total = total * base + value
    return total
