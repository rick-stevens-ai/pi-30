# P12 SEED: only base 10. to_base ignores base; parse_int uses int(s) base-10.
def to_base(n, base):
    if base < 2 or base > 36:
        raise ValueError("base must be 2..36")
    
    digits = '0123456789abcdefghijklmnopqrstuvwxyz' 
    
    if n == 0:
        return '0'
    
    sign = ''
    if n < 0:
        sign = '-'
        n = -n
    
    res = ''
    while n > 0:
        res = digits[n % base] + res
        n = n // base
    
    return sign + res

def parse_int(s, base):
    if base < 2 or base > 36:
        raise ValueError("base must be 2..36")
    
    digits = '0123456789abcdefghijklmnopqrstuvwxyz' 
    
    if s == '':
        raise ValueError("empty string")
    
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    
    num = 0
    for c in s:
        if c not in digits:
            raise ValueError(f"invalid character {c}")
        
        val = digits.index(c)
        num = num * base + val
    
    return sign * num
