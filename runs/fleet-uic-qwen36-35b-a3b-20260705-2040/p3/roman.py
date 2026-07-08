def to_roman(n):
    if not 1 <= n < 4000:
        raise ValueError("n out of range")
    vals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = []
    for value, numeral in vals:
        while n >= value:
            result.append(numeral)
            n -= value
    return ''.join(result)

def from_roman(s):
    roman_vals = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    result = 0
    prev = 0
    for ch in reversed(s):
        val = roman_vals[ch]
        if val < prev:
            result -= val
        else:
            result += val
        prev = val
    return result
