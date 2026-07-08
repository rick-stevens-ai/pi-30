import math

def softmax(x):
    """
    Compute softmax values for a list of scores with numerical stability.
    
    The softmax function computes: softmax(x_i) = exp(x_i) / sum(exp(x_j))
    
    For numerical stability, we subtract the max value from all elements
    before exponentiating: softmax(x_i) = exp(x_i - max(x)) / sum(exp(x_j - max(x)))
    
    Args:
        x: List of float values
        
    Returns:
        List of softmax probabilities summing to 1.0
    """
    if not x:
        return []
    
    # Find max for numerical stability
    max_val = max(x)
    
    # Compute exponentials with numerical stability
    exp_values = [math.exp(x_i - max_val) for x_i in x]
    
    # Sum of exponentials
    sum_exp = sum(exp_values)
    
    # Handle edge case where all values are -inf (sum_exp == 0)
    if sum_exp == 0:
        # Return uniform distribution
        n = len(x)
        return [1.0 / n] * n
    
    # Compute softmax probabilities
    return [exp_val / sum_exp for exp_val in exp_values]


def softmax_stable(x):
    """
    Alias for softmax - numerically stable softmax implementation.
    """
    return softmax(x)


if __name__ == "__main__":
    # Simple test
    test_cases = [
        [1.0, 2.0, 3.0],
        [1000.0, 2000.0, 3000.0],  # Large values - test numerical stability
        [-1000.0, -2000.0, -3000.0],  # Large negative values
        [1.0, 1.0, 1.0],  # Equal values
        [],  # Empty list
        [0.0],  # Single element
        [-1000.0, 0.0, 1000.0],  # Mixed large values
    ]
    
    for test in test_cases:
        result = softmax(test)
        print(f"Input: {test}")
        print(f"Output: {result}")
        print(f"Sum: {sum(result):.10f}")
        print()
