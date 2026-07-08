import numpy as np

def softmax(x):
    """
    Computes the softmax of the input vector x in a numerically stable way.
    
    Args:
        x (np.ndarray): The input vector of scores or logits.

    Returns:
        np.ndarray: The softmax probabilities.
    """
    # Subtract the maximum value for numerical stability to prevent overflow
    x_max = np.max(x)
    exps = np.exp(x - x_max)
    return exps / np.sum(exps)

if __name__ == '__main__':
    # Example usage (for testing purposes)
    test_input = np.array([1.0, 2.0, 3.0])
    result = softmax(test_input)
    print(f"Input: {test_input}")
    print(f"Softmax result: {result}")