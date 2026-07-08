# P12: base-N integer arithmetic for bases 2..36
def to_base(n, base):
    if not 2 <= base <= 36:
        raise ValueError(f"base must be between 2 and 36, got {base}")
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    neg = n < 0
    n = -n if neg else n
    result = []
    while n > 0:
        n, rem = divmod(n, base)
        result.append(digits[rem])
    if neg:
        result.append("-")
    return "".join(reversed(result))

def parse_int(s, base):
    if not 2 <= base <= 36:
        raise ValueError(f"base must be between 2 and 36, got {base}")
    return int(s, base)
