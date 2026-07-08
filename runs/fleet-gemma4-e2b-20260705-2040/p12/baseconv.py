def to_base(n, base):
    if n == 0:
        return "0"
    is_negative = n < 0
    n = abs(n)

    # Digits for bases up to 36 (0-9, a-z)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""

    while n > 0:
        remainder = n % base
        result = digits[remainder] + result
        n //= base

    if is_negative:
        return "-" + result
    else:
        return result

def parse_int(s, base):
    s = s.strip()
    if not s:
        raise ValueError("Input string cannot be empty")

    # Digits for bases up to 36 (0-9, a-z)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    value = 0
    power = 0

    for char in reversed(s):
        if char not in digits:
            raise ValueError(f"Invalid character '{char}' for base {base}")

        digit_value = digits.index(char)
        if digit_value >= base:
             raise ValueError(f"Digit value {digit_value} is too large for base {base}")

        value += digit_value * (base ** power)
        power += 1

    return value