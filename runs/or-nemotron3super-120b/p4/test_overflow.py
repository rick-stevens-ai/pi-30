from fast import softmax
import math

# Test overflow case
print("Testing large numbers:")
print(softmax([1000.0, 1001.0, 1002.0]))
print("Sum:", sum(softmax([1000.0, 1001.0, 1002.0])))

# Test underflow case
print("\nTesting very negative numbers:")
print(softmax([-1000.0, -1000.0, -999.0]))
print("Sum:", sum(softmax([-1000.0, -1000.0, -999.0])))

# Test mixed
print("\nTesting mixed:")
print(softmax([1e3, -1e3, 0.0]))
print("Sum:", sum(softmax([1e3, -1e3, 0.0])))

# Test that no NaN or Inf appears
for xs in [[1000.0, 1001.0, 1002.0], [-1000.0, -1000.0, -999.0], [0.0,0.0,0.0]]:
    out = softmax(xs)
    if any(math.isnan(x) or math.isinf(x) for x in out):
        print("Bad output for", xs)
    else:
        print("OK for", xs)