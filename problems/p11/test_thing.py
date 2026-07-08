# P11 iterate-until-green: balanced-parens / expression validator.
# Seed handles ( ) only; tests require (), [], {} matching + rejects mismatches.
from parens import is_balanced
import pytest

cases = [
    ("", True), ("()", True), ("()[]{}", True), ("([{}])", True),
    ("(]", False), ("([)]", False), ("{[}", False), ("(((", False),
    (")))", False), ("a(b)c[d]{e}", True), ("foo(bar[baz])", True),
    ("(()", False), ("())", False), ("{[()()]}", True), ("][", False),
]

@pytest.mark.parametrize("s,ok", cases)
def test_balanced(s, ok):
    assert is_balanced(s) == ok
