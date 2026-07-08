import math

def softmax(xs):
    """Numerically stable softmax operator.
    
    Args:
        xs: iterable of numbers (floats).
        
    Returns:
        list[float]: Probabilities that sum to 1.0, computed with
          shifted exponentials for numerical stability.
    """
    # Find max value for shifting to avoid overflow in exp()
    max_x = max(xs)
    # Compute e^(x_i - max_x) safely
    exps = [math.exp(v - max_x) for v in xs]
    sum_exps = sum(exps)
    # Normalize: divide each exponentiated value by the total sum
    return [v / sum_exps for v in exps]