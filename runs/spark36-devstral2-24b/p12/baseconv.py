# P12 SEED: only base 10. to_base ignores base; parse_int uses int(s) base-10.
import string

# Digits for bases 2-36
DIGITS = string.digits + string.ascii_lowercase

def to_base(n, base):
    """Convert integer n to lowercase string in given base (2-36)"""
    if n == 0:
        return "0"
    
    is_negative = n < 0
    n = abs(n)
    
    digits = []
    while n > 0:
        remainder = n % base
        digits.append(DIGITS[remainder])
        n = n // base
    
    if is_negative:
        digits.append('-')
    
    return ''.join(reversed(digits))

def parse_int(s, base):
    """Convert lowercase string in given base (2-36) to integer"""
    # Map character to its value
    char_map = {ch: idx for idx, ch in enumerate(DIGITS)}
    
    if s.startswith('-'):
        is_negative = True
        s = s[1:]
    else:
        is_negative = False
    
    result = 0
    for ch in s:
        result = result * base + char_map[ch]
    
    return -result if is_negative else result
