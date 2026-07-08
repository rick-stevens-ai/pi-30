# -*- coding: utf-8 -*-
"""Convert to and from Roman numerals using subtractive notation."""


def _numeral_map():
    return (
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
        ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
        ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1),
    )


def to_roman(n):
    """Convert an integer to a Roman numeral string."""
    result = ''
    for numeral, value in _numeral_map():
        while n >= value:
            result += numeral
            n -= value
    return result


# Pattern for validating Roman numerals (subtractive notation)
import re

_roman_pattern = re.compile(
    r"""^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$""",
    re.VERBOSE,
)


def from_roman(s):
    """Convert a Roman numeral string to an integer."""
    if not s:
        raise ValueError('Input can not be blank')
    if _roman_pattern.search(s) is None:
        raise ValueError('Invalid Roman numeral: %s' % s)

    result = 0
    index = 0
    for numeral, value in _numeral_map():
        while s[index:index + len(numeral)] == numeral:
            result += value
            index += len(numeral)
    return result


class RomanError(Exception):
    pass


class OutOfRangeError(RomanError):
    def __init__(self, msg='number out of range (must be 0..4999)'):
        super().__init__(msg)


class NotIntegerError(RomanError):
    def __init__(self, msg='decimals can not be converted'):
        super().__init__(msg)


class InvalidRomanNumeralError(RomanError):
    pass
