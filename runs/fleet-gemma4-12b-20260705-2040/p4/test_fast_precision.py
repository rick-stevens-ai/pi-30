import math
from fast import softmax as fast_softmax
from decimal import Decimal, getcontext

getcontext().prec = 60

def ref_softmax(xs):
    m = max(xs)
    # We have to fix the TypeError here for our local test since we can't edit check.py
    # But wait, if I change it here, it doesn't mean check.py is fixed.
    # The goal is to make fast.py match check.py (once check.py is "fixed" or bypassed).
    # Actually, the user says DO NOT edit check.py. 
    # This implies that I should make fast.py such that it doesn't cause issues.
    
    # Let's see what happens if we use Decimal correctly here just to know the expected output.
    m_dec = Decimal(str(m))
    exps = [Decimal(str(v)) - m_dec for v in xs] # this is not quite right, ref_softmax does something else
    # Let's look at check.py again:
    # exps = [Decimal(x - m).exp() for x in [Decimal(v) for v in xs]]
    # where x is Decimal(v) and m is max(xs) (float).
    # So it's trying to do Decimal - float.
    pass

# Since I can't edit check.py, I should try to understand why fast.py would disagree.
# Maybe the issue is with precision? 
# Or maybe I should use math.exp(x - max_x) but handle the case where sum_exps is zero?
