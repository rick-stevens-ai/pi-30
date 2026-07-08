# P13 iterate-until-green: a tiny JSON-subset parser (no eval, no json module).
# Supports null/true/false, ints, floats, strings, arrays, objects, nesting,
# whitespace. Seed only parses ints. Verdict = pytest exit code.
from miniparse import parse
import pytest

cases = [
    ("null", None), ("true", True), ("false", False),
    ("0", 0), ("42", 42), ("-7", -7), ("3.14", 3.14),
    ('"hi"', "hi"), ('""', ""), ('"a b"', "a b"),
    ("[]", []), ("[1,2,3]", [1, 2, 3]), ("[1, 2, 3]", [1, 2, 3]),
    ("{}", {}), ('{"a":1}', {"a": 1}), ('{"a": 1, "b": 2}', {"a": 1, "b": 2}),
    ('[1, [2, [3]]]', [1, [2, [3]]]),
    ('{"x": [1, {"y": true}], "z": null}', {"x": [1, {"y": True}], "z": None}),
    ('  [ 1 , 2 ]  ', [1, 2]),
]

@pytest.mark.parametrize("s,want", cases)
def test_parse(s, want):
    assert parse(s) == want
