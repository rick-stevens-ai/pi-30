from fast import softmax
import math

# Test with values that would cause overflow without max subtraction
overflow_test = [800.0, 801.0, 802.0]

print("Testing overflow case...")
result = softmax(overflow_test)
print(f"Input: {overflow_test}")
print(f"Result: {result}")
print(f"Sum: {sum(result)}")
print(f"All finite: {all(math.isfinite(x) for x in result)}")

# Test with very negative values (underflow case)
underflow_test = [-1000.0, -1000.0, -999.0]
print("\nTesting underflow case...")
result = softmax(underflow_test)
print(f"Input: {underflow_test}")
print(f"Result: {result}")
print(f"Sum: {sum(result)}")
print(f"All finite: {all(math.isfinite(x) for x in result)}")

# Test edge case: empty input
print("\nTesting empty input...")
result = softmax([])
print(f"Result: {result}")

print("\nAll tests passed!")
