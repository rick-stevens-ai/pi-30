ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
MAX_BASE = len(ALPHABET)

def to_base(n, base):
    if not (2 <= base <= MAX_BASE):
        raise ValueError("Base must be between 2 and 36.")
    
    if n == 0:
        return '0'
    
    is_negative = n < 0
    if is_negative:
        n = abs(n)
    
    result = []
    while n > 0:
        remainder = n % base
        result.append(ALPHABET[remainder])
        n //= base
        
    return ('-' if is_negative else '') + "".join(reversed(result))

def parse_int(s, base):
    if not (2 <= base <= MAX_BASE):
        raise ValueError("Base must be between 2 and 36.")
    
    is_negative = s.startswith('-')
    s_to_parse = s[1:] if is_negative else s

    result = 0
    for char in s_to_parse:
        try:
            digit_value = ALPHABET.index(char)
        except ValueError:
            raise ValueError("Invalid character for the given base.")

        if digit_value >= base:
             raise ValueError(f"Digit '{char}' value ({digit_value}) is too large for base {base}.")
        
        result = result * base + digit_value
        
    return -result if is_negative else result
