def to_roman(n):
    mapping = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = ""
    for value, symbol in mapping:
        while n >= value:
            result += symbol
            n -= value
    return result

def from_roman(s):
    mapping = {
        'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
        'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
        'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
    }
    result = 0
    i = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in mapping:
            result += mapping[s[i:i+2]]
            i += 2
        else:
            result += mapping[s[i]]
            i += 1
    return result
