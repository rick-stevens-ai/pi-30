ROMAN_VALUES = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
SUBTRACTIVE = {'CM': 900, 'CD': 400, 'XC': 90, 'XL': 40, 'IX': 9, 'IV': 4}
ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def to_roman(n):
    result = []
    for value, symbol in ROMAN_MAP:
        while n >= value:
            result.append(symbol)
            n -= value
    return ''.join(result)

def from_roman(s):
    result = 0
    i = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in SUBTRACTIVE:
            result += SUBTRACTIVE[s[i:i+2]]
            i += 2
        else:
            result += ROMAN_VALUES[s[i]]
            i += 1
    return result