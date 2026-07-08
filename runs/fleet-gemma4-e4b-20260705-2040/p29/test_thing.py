# P29 iterate-until-green: a shunting-yard / recursive-descent arithmetic
# evaluator. evaluate(expr) handles + - * / ( ) with correct precedence and
# associativity, integer and float, unary minus. Seed only does left-to-right
# single-op. No eval() allowed. Verdict = pytest exit code.
from calc import evaluate
import pytest

cases = [
    ("1+1", 2), ("2*3+4", 10), ("2+3*4", 14), ("(2+3)*4", 20),
    ("10-2-3", 5), ("100/4/5", 5), ("2*(3+(4-1))", 12),
    ("-5+3", -2), ("-(2+3)", -5), ("3*-2", -6),
    ("1+2*3-4/2", 5), ("((1+2)*(3+4))", 21), ("7", 7),
    ("2*3*4", 24), ("8/2*2", 8),
]

@pytest.mark.parametrize("expr,want", cases)
def test_eval(expr, want):
    assert abs(evaluate(expr) - want) < 1e-9
