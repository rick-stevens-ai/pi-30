
"""Convert to and from Roman numerals"""

__author__   = "Mark Pilgrim (f8dy@diveintopython.org)"
__version__  = "1.4"
__date__     = "8 August 2001"
__copyright__= """Copyright  (c) 2001 Mark Pilgrim
This program is part of \"Dive Into Python\", a free Python tutorial for experienced programmers. Visit http://diveintopython.org/ for the latest version."""
import argparse
import re
import sys


# Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass


# Digit mapping with subtractive notation: 
romanNumeralMap = (
     ('M', 1000),
     ('CM', 900),
     ('D', 500),
     ('CD', 400),
     ('C', 100),
     ('XC', 90),
     ('L', 50),
     ('XL', 40),
     ('X', 10),
     ('IX', 9),
     ('V', 5),
     ('IV', 4),
     ('I', 1)
)


def to_roman(n): 
    """Convert integer to Roman numeral."""
    if not isinstance(n, int):
        raise NotIntegerError("decimals can not be converted")
    if not (-1 < n < 5000): 
        raise OutOfRangeError("number out of range (must be 0..4999)")
  
    # special case
    if n == 0:
        return 'N'

    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result


# Pattern to validate Roman numerals.
romanNumeralPattern = re.compile("""
^                     # start of string
M{0,4}                  # thousands - 0 to 4 Ms
(?:CM|CD|D?C{0,3})      # hundreds - 900 (CM), 400 (CD), or 0-300 (C*C*C) or 500-800 (D + C{C,C,C})
(?:XC|XL|L?X{0,3})      # tens - 90 (XC), 40 (XL), or 0-3 (XXX.. or L followed by Xs)
(?:IX|IV|V?I{0,3})       # ones - 9 (IX), 4 (IV), or 0-3 (IIII or V + III)
$                       # end of string
""", re.VERBOSE)

def from_roman(s):
    """Convert Roman numeral to integer."""
    if not s:
        raise InvalidRomanNumeralError('Input cannot be blank')
    if s == 'N':
        return 0
    if not romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError('Invalid Roman numeral: %s' % s)

    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result

def parse_args():
    parser = argparse.ArgumentParser(
        prog='roman',
        description='convert between roman and arabic numerals'
    )
    parser.add_argument('number', help='the value to convert')
    parser.add_argument('-r','--reverse',
        action='store_true',
        default=False,
        help='convert roman to numeral (case insensitive) [default: False]') 
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.reverse:
        u = args.number.upper()
        r = from_roman(u)
        print(r)
    else:
        i = int(args.number)
        n = to_roman(i)
        print(n)
    return 0

if __name__ == '__main__':
    sys.exit(main())