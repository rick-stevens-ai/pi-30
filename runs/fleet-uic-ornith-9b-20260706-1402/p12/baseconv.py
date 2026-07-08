# P12: base-N integer arithmetic for bases 2..36.
_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    if n == 0:
        return "0"
    neg = n < 0
    n = -n if neg else n
    digits = []
    while n > 0:
        digits.append(_DIGITS[n % base])
        n //= base
    result = "".join(reversed(digits))
    return "-" + result if neg else result


def parse_int(s, base):
    s = s.strip()
    neg = False
    if s[0] == "-":
        neg = True
        s = s[1:]
    elif s[0] == "+":
        s = s[1:]

    value = 0
    for ch in s:
        idx = _DIGITS.index(ch.lower())
        if idx >= base:
            raise ValueError(f"Invalid digit '{ch}' for base {base}")
        value = value * base + idx

    return -value if neg else value
