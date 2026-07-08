def to_roman(num):
    """Converts an integer to a Roman numeral string, supporting subtractive notation."""
    if not isinstance(num, int) or num <= 0 or num >= 4000:
        raise ValueError("Input must be a positive integer less than 4000.")

    mapping = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'
    }

    roman_numeral = ""
    for value, symbol in mapping.items():
        while num >= value:
            roman_numeral += symbol
            num -= value
    return roman_numeral

def from_roman(s):
    """Converts a Roman numeral string to an integer."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    i = 0
    while i < len(s):
        current_value = roman_map[s[i]]
        # Check if the next symbol exists and is larger (subtractive notation)
        if i + 1 < len(s) and current_value < roman_map[s[i+1]]:
            result += (roman_map[s[i+1]] - current_value)
            i += 2 # Skip both symbols
        else:
            result += current_value
            i += 1
    return result