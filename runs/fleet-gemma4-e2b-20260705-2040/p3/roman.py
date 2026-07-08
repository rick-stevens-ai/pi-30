def to_roman(num: int) -> str:
    """Converts an integer to a Roman numeral string."""
    if not 1 <= num < 4000:
        raise ValueError("Input must be between 1 and 3999")

    roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = ""
    for value, symbol in roman_map:
        while num >= value:
            result += symbol
            num -= value
    return result

def from_roman(roman_numeral: str) -> int:
    """Converts a Roman numeral string to an integer."""
    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    
    value = 0
    i = 0
    while i < len(roman_numeral):
        current_val = roman_map[roman_numeral[i]]
        
        if i + 1 < len(roman_numeral):
            next_val = roman_map[roman_numeral[i+1]]
            if current_val < next_val:
                value += next_val - current_val
                i += 2
            else:
                value += current_val
                i += 1
        else:
            value += current_val
            i += 1
    return value