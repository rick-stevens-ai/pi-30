def to_base(n, base):
    # Validate base range
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")
    # Handle sign
    neg = n < 0
    n_abs = -n if neg else n
    # Special case zero
    if n_abs == 0:
        return "0"
    digits = []
    while n_abs > 0:
        rem = n_abs % base
        # Convert remainder to character
        if rem < 10:
            ch = str(rem)
        else:
            ch = chr(ord('a') + rem - 10)  # lowercase a-z
        digits.append(ch)
        n_abs //= base
    # Reverse list
    result = ''.join(reversed(digits))
    return "-" + result if neg else result


def parse_int(s, base):
    # Validate base range
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
    # Sign handling
    sign = 1
    if s[0] == '+':
        s = s[1:]
    elif s[0] == '-':
        sign = -1
        s = s[1:]
    if not s:
        raise ValueError("No digits after sign")
    # Parse digits
    value = 0
    for ch in s:
        # Convert character to numeric digit
        if '0' <= ch <= '9':
            digit = ord(ch) - ord('0')
        elif 'a' <= ch <= 'z':
            digit = ord(ch) - ord('a') + 10
        else:
            raise ValueError(f"Invalid character '{ch}' for base {base}")
        if digit >= base:
            raise ValueError(f"Digit '{ch}' out of range for base {base}")
        value = value * base + digit
    return sign * value