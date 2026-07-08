import numpy as np

def softmax(X):
    # Numerical stability trick: subtract max before exponentiation
    max_val = np.max(X)
    e_x = np.exp(X - max_val)
    return e_x / np.sum(e_x)