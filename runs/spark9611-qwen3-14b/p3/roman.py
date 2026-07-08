def to_roman(n):
    roman_numerals = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 
        100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 
        10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'
    }
    result = ''
    for value, symbol in roman_numerals.items():
        while n >= value:
            result += symbol
            n -= value
    return result

def from_roman(s):
    roman_numerals = {
        'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
        'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
        'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
    }
    total = 0
    i = 0
    while i < len(s):
        if i+1 < len(s) and s[i:i+2] in roman_numerals:
            total += roman_numerals[s[i:i+2]]
            i += 2
        else:
            total += roman_numerals[s[i]]
            i += 1
    return total