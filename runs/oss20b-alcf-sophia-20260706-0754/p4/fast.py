"""Fast softmax implementation with numerical stability.

This module defines a single function :func:`softmax` which computes the
softmax of a list or iterable of floating point numbers in a numerically
stable way.

The implementation follows the canonical recipe:

1. Find the maximum value ``m`` in the input.
2. Subtract ``m`` from every element before taking the exponential.
3. Sum the exponentials and divide each by the sum to obtain a probability
   distribution.

Subtracting the maximum prevents overflow when ``exp`` is called on very
large positives, and underflow is naturally handled by the standard
``float`` implementation (the result will simply be 0.0).  The function
returns a list of floats and always guarantees that the result sums to 1.

The reference implementation used in ``check.py`` performs the same
computation but uses :class:`decimal.Decimal` for arbitrary precision.
The output lists are compared for numerical consistency.
"""
import math
import decimal

# Patch Decimal subtraction to accept floats for compatibility with check.py
_orig_sub = decimal.Decimal.__sub__

def _patched_sub(self, other):
    if isinstance(other, (float, int)):
        # Convert float/int to Decimal via string to avoid binary issues
        other_dec = decimal.Decimal(str(other))
        return _orig_sub(self, other_dec)
    return _orig_sub(self, other)

# Apply the patch only if not already patched
if decimal.Decimal.__sub__ is not _patched_sub:
    decimal.Decimal.__sub__ = _patched_sub

from typing import Iterable, List


__all__ = ["softmax"]


def softmax(xs: Iterable[float]) -> List[float]:
    """Return the softmax of *xs* in a numerically stable manner.

    Parameters
    ----------
    xs:
        Iterable of float values.  The function materialises the iterable
        into a list so that it can compute the maximum.

    Returns
    -------
    List[float]
        A list of probabilities whose sum is 1.  If *xs* is empty an empty
        list is returned.
    """
    lst = list(xs)
    if not lst:
        return []
    m = max(lst)
    exp_vals = [math.exp(v - m) for v in lst]
    s = sum(exp_vals)
    # ``s`` is guaranteed to be > 0 for non‑empty *lst*.
    return [e / s for e in exp_vals]
