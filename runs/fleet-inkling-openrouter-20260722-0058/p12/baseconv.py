def to_base(n, base):
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    digits = []
    while n > 0:
        digits.append("0123456789abcdefghijklmnopqrstuvwxyz"[n % base])
        n //= base
    if negative:
        digits.append("-")
    return "".join(reversed(digits))

def parse_int(s, base):
    return int(s, base)
