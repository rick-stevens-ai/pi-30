import math
from decimal import Decimal
import builtins

def _monkeypatch_decimal():
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

if __name__ == "__main__":
    try:
        print(f"Result 1: {softmax([800.0, 801.0, 802.0])}")
        print(f"Result 2: {softmax([-1000.0, -1000.0, -999.0])}")
    except Exception as e:
        print(f"Error: {e}")
