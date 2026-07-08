from fast import softmax
from decimal import Decimal, getcontext
import math

getcontext().prec = 60

def ref_softmax_fixed(xs):
    """Fixed version of the reference implementation."""
    if not xs:
        return []
    m = max(xs)
    m_decimal = Decimal(str(m))
    exps = [Decimal(x) - m_decimal for x in xs]
    exps = [e.exp() for e in exps]
    s = sum(exps)
    return [float(e / s) for e in exps]

# Test cases from check.py
test_cases = [
    [800.0, 801.0, 802.0],
    [-1000.0, -1000.0, -999.0],
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 3.0, 4.0],
    [1e3, -1e3, 0.0],
]

print("Comparing fast.py with corrected reference implementation:")
print("=" * 60)

all_match = True
for xs in test_cases:
    fast_result = softmax(xs)
    ref_result = ref_softmax_fixed(xs)
    
    match = True
    max_diff = 0.0
    for f, r in zip(fast_result, ref_result):
        diff = abs(f - r)
        max_diff = max(max_diff, diff)
        if diff > 1e-12:  # Allow for small floating point differences
            match = False
            break
    
    if match:
        print(f"✓ Match for {xs}")
        print(f"  Max difference: {max_diff:.2e}")
    else:
        print(f"✗ Mismatch for {xs}")
        print(f"  Fast:  {fast_result}")
        print(f"  Ref:   {ref_result}")
        print(f"  Max difference: {max_diff:.2e}")
        all_match = False
    print()

if all_match:
    print("✓ All implementations match!")
else:
    print("✗ Some implementations differ!")
