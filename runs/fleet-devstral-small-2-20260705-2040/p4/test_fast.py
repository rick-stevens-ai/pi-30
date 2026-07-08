import math
from fast import softmax

# Test cases
test_cases = [
    [800.0, 801.0, 802.0],
    [-1000.0, -1000.0, -999.0],
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 3.0, 4.0],
    [1e3, -1e3, 0.0],
]

for xs in test_cases:
    result = softmax(xs)
    print(f"Input: {xs}")
    print(f"Result: {result}")
    print(f"Sum: {sum(result)}")
    print(f"All finite: {all(math.isfinite(x) for x in result)}")
    print()
