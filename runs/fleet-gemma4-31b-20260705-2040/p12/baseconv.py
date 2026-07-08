def to_base(n, base):
    if n == 0:
        return "0"
    
    negative = n < 0
    n = abs(n)
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    res = []
    while n > 0:
        res.append(digits[n % base])
        n //= base
    
    s = "".join(reversed(res))
    return "-" + s if negative else s

def parse_int(s, base):
    return int(s, base)
