# P3 verifier — DO NOT let the agent edit this file.
# Tests a Roman-numeral <-> int round trip plus tricky subtractive cases.
from roman import to_roman, from_roman
import pytest

cases = [
    (1, "I"), (4, "IV"), (9, "IX"), (14, "XIV"), (40, "XL"),
    (90, "XC"), (400, "CD"), (900, "CM"), (1994, "MCMXCIV"),
    (2023, "MMXXIII"), (3888, "MMMDCCCLXXXVIII"), (49, "XLIX"),
]

@pytest.mark.parametrize("n,s", cases)
def test_to_roman(n, s):
    assert to_roman(n) == s

@pytest.mark.parametrize("n,s", cases)
def test_from_roman(n, s):
    assert from_roman(s) == n

def test_round_trip():
    for n in range(1, 4000):
        assert from_roman(to_roman(n)) == n
