import math
from fast import softmax

inputs = [
    [800.0, 801.0, 802.0],          # forces overflow in naive exp
    [-1000.0, -1000.0, -999.0],      # forces underflow to all-zero / nan
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 3.0, 4.0],
    [1e3, -1e3, 0.0],
]

for xs in inputs:
    print(f"Input: {xs}")
    try:
        got = softmax(xs)
        print(f"Got:  {got}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
