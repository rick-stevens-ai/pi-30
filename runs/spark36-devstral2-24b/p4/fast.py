import math

def softmax(xs):
    """
    Numerically stable softmax implementation.
    Subtracts max before exp to avoid overflow.
    """
    if not xs:
        return []
    
    # Find the maximum value for numerical stability
    m = max(xs)
    
    # Compute exponentials of (x - max) and their sum
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    
    # Return normalized probabilities
    return [e / s for e in exps]
