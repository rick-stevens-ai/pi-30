def to_base(n, base):
    if n == 0:
        return '0'
    negative = n < 0
    digits = ''
    while n != 0:
        n, r = divmod(n, base)
        digits += '0123456789abcdefghijklmnopqrstuvwxyz'[r]
    result = ''.join(reversed(digits))
    return '-' + result if negative else result


def parse_int(s, base):
    return int(s, base)
