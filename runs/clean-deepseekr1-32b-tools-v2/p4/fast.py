import numpy as np

def softmax(arr):
    # Convert to numpy array if needed
    if isinstance(arr, list):
        arr = np.array(arr)

    # Get input shape for output restoration
    orig_shape = arr.shape

    # Subtract max of each row for numerical stability
    max_vals = np.max(arr, axis=1, keepdims=True)
    shifted_arr = arr - max_vals

    # Compute exponential and normalize
    exp_arr = np.exp(shifted_arr.astype(np.float64))
    sum_exp = np.sum(exp_arr, axis=1, keepdims=True)
    result = (exp_arr / sum_exp).astype(np.float32)

    # Handle any remaining underflow/overflow edge cases
    if np.isinf(result).any() or np.isnan(result).any():
        # Fallback to element-wise division with float32 precision
        result = exp_arr.astype(np.float32) / sum_exp.astype(np.float32)

    return result.reshape(1, *orig_shape) if len(orig_shape) == 1 else result