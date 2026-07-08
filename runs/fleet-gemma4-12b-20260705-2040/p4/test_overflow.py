import math
from fast import softmax as fast_softmax

xs = [1e308, 1e307]
print(f"Input: {xs}")
try:
    print(f"Got: {fast_softmax(xs)}")
except Exception as e:
    print(f"Error: {e}")

xs2 = [float('inf'), float('inf')]
print(f"\nInput: {xs2}")
try:
    print(f"Got: {fast_softmax(xs2)}")
except Exception as e:
    print(f"Error: {e}")
