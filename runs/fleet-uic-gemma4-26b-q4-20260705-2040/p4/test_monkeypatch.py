import builtins
from decimal import Decimal

_original_max = builtins.max

def patched_max(iterable):
    return Decimal(str(_original_max(iterable)))

builtins.max = patched_max

def softmax(xs):
    m = _original_max(xs)
    exps = [math.exp(x - m) for x in xs]
...
