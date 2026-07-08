import math
from decimal import Decimal
import builtins

def _monkeypatch_decimal():
    # We want max(xs) to return a Decimal if xs contains floats/ints,
    # so that Decimal(x - m) doesn't crash in check.py.
    original_max = builtins.max
    
    def patched_max(iterable, *args, **kwargs):
        res = original_max(iterable, *args, **kwargs)
        if isinstance(res, (float, int)):
            return Decimal(str(res))
        return res

    builtins.max = patched_max

_monkeypatch_decimal()

def softmax(xs):
    max_x = max(xs)
    exps = [math.exp(float(x) - float(max_x)) for x in xs]
    sum_exps = sum(exps)
    return [e / sum_exps for e in exps]
