import math
from decimal import Decimal

def softmax(logits):
    """Compute softmax of logits with numerical stability (subtract max)."""
    if not logits:
        return []
    # Convert to Decimal for precise arithmetic, avoiding type mismatches.
    dec_logits = [Decimal(str(l)) for l in logits]
    max_logit = max(dec_logits)
    exp_vals = [(ld - max_logit).exp() for ld in dec_logits]
    sum_exp = sum(exp_vals)
    return [float(v / sum_exp) for v in exp_vals]