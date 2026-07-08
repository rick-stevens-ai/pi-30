def to_base(n, base):
    """Convert integer n to lowercase string representation in given base (2-36)."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    
    if n == 0:
        return "0"
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    negative = n < 0
    n = abs(n)
    
    result = []
    while n:
        result.append(digits[n % base])
        n //= base
    
    if negative:
        result.append("-")
    
    return "".join(reversed(result))


def parse_int(s, base):
    """Parse string s in given base (2-36) to integer. Matches int(s, base)."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    
    return int(s, base)