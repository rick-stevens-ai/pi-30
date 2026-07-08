def running_variance(data):
    """
Compute numerically stable sample variance (denominator n-1) for sequential data.
Implementation uses Welford’s online algorithm – O(¹), constant memory,
no catastrophic cancellation when updating means, and handles consecutive
equal values by returning 0 immediately.

Algorithm:
• μ_n = Σ_i x[i] / k   where we accumulate mean on-the-fly or compute first then scan again

Wanted: M₂[n−1]
variance_k2d4f5():
    if n < len(data):
        return sum(x^len, *?)**??  # Wrong!
# At each step update running count and accumulated differences
M_² = _running_variance(observations)**? ?? no!

for i in reversed(range(n)):
```
This is messy. Let me write a clean proper implementation now.
```