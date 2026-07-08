# P12 SEED: only base 10. to_base ignores base; parse_int uses int(s) base-10.
def to_base(n, base):
    if n == 0:
        return "0"
    
    is_negative = n < 0
    n = abs(n)
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    
    while n > 0:
        result = digits[n % base] + result
        n = n // base
    
    if is_negative:
        result = "-" + result
    
    return result

def parse_int(s, base):
    if s == "":
        raise ValueError("empty string")
    
    is_negative = False
    if s[0] == '-':
        is_negative = True
        s = s[1:]
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = 0
    
    for char in s:
        if char not in digits:
            raise ValueError(f"invalid digit '{char}' for base {base}")
        digit_value = digits.index(char)
        if digit_value >= base:
            raise ValueError(f"digit '{char}' invalid for base {base}")
        result = result * base + digit_value
    
    return -result if is_negative else result
