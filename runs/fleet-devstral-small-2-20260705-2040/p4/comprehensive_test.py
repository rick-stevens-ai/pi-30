from fast import softmax
import math

def test_softmax():
    """Comprehensive test of the softmax implementation."""
    
    test_cases = [
        # Basic cases
        ([1.0, 2.0, 3.0], "basic case"),
        ([0.0, 0.0, 0.0], "all zeros"),
        ([1.0, 1.0, 1.0], "all ones"),
        
        # Edge cases
        ([], "empty input"),
        ([1.0], "single element"),
        ([1.0, -1.0], "positive and negative"),
        
        # Numerical stability cases
        ([800.0, 801.0, 802.0], "large values (overflow test)"),
        ([-1000.0, -1000.0, -999.0], "very negative values (underflow test)"),
        ([1e3, -1e3, 0.0], "mixed extreme values"),
        
        # Precision cases
        ([1.0, 2.0, 3.0, 4.0, 5.0], "five elements"),
        ([0.1, 0.2, 0.3, 0.4, 0.5], "small values"),
    ]
    
    all_passed = True
    
    for inputs, description in test_cases:
        try:
            result = softmax(inputs)
            
            # Check basic properties
            if len(result) != len(inputs):
                print(f"FAIL: {description} - length mismatch")
                all_passed = False
                continue
                
            if not all(math.isfinite(x) for x in result):
                print(f"FAIL: {description} - contains NaN or Inf")
                all_passed = False
                continue
                
            # Skip sum check for empty input
            if len(result) > 0:
                sum_result = sum(result)
                if not math.isclose(sum_result, 1.0, rel_tol=1e-9):
                    print(f"FAIL: {description} - sum is {sum_result}, not 1.0")
                    all_passed = False
                    continue
                    
                # Check that all values are non-negative
                if any(x < 0 for x in result):
                    print(f"FAIL: {description} - contains negative values")
                    all_passed = False
                    continue
            
            print(f"PASS: {description}")
            
        except Exception as e:
            print(f"ERROR: {description} - {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    test_softmax()
