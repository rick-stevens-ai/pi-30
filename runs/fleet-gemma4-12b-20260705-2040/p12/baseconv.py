# P12 SEED: only base 10. to_base ignores base; parse_int uses int(s) base-10.
def to_base(n, base):
    if n == 0:
        return "0"
    
    negative = n < 0
    n = abs(n)
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    res = ""
    while n > 0:
        res = digits[n % base] + res
        n //= base
    
    return ("-" if negative else "") + res

def parse_int(s, base):
    return int(s, base)
