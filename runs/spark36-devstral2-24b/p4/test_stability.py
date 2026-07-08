import math

def test_overflows():
    # Test cases that would overflow without max subtraction
    test_cases = [
        [800.0, 801.0, 802.0],
        [-1000.0, -1000.0, -999.0],
    ]
    
    for i, xs in enumerate(test_cases):
        print(f"Test case {i+1}: {xs}")
        result = softmax(xs)
        print(f"  Result: {result}")
        print(f"  Sum: {sum(result)}")
        for val in result:
            if math.isnan(val) or math.isinf(val):
                print("  ERROR: NaN or Inf detected!")
            else:
                print(f"  All values are finite")
        print()

if __name__ == "__main__":
    test_overflows()