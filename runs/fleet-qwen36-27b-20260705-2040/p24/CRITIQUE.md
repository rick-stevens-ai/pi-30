NO_ISSUES

## Summary

Reviewed `limiter.py` (TokenBucket + RateLimiter) for three defect classes:
burst-exceeds-capacity, wrong refill math, and clock misuse.

### Burst-exceeds-capacity — Clean

- `TokenBucket.__init__` sets `self.tokens = float(capacity)` (full at start).
- Every refill in `allow()` is clamped: `min(self.capacity, …)`.
- Tokens are only deducted when `self.tokens >= n`, so `tokens` never goes negative.
- `RateLimiter` sets `capacity=rate`, matching the documented "full window quota" semantics.

No path exists where the bucket can hold or dispense more than `capacity` tokens.

### Wrong refill math — Clean

- Refill formula `self.tokens + elapsed * self.rate` is correct: tokens added = elapsed seconds × tokens/second.
- `round(…, 10)` mitigates floating-point accumulation noise (e.g., 0.4 × 5 → 1.999…).
- `min(self.capacity, …)` prevents overfill beyond capacity.
- `RateLimiter` constructs the bucket with `rate=rate/per` (tokens/sec) and `capacity=rate` (full-window tokens), which is arithmetically consistent.

The docstring's "recompute from scratch" wording is slightly misleading (the refill is actually incremental with rounding, not a deficit-from-scratch calculation), but the math itself is correct.

### Clock misuse — Clean

- `self.last_time = clock()` at construction establishes a proper baseline.
- `elapsed = max(0.0, now - self.last_time)` correctly guards against clock reversal (backwards tick → elapsed treated as 0, no over-refill).
- `self.last_time = now` is updated on every call, so subsequent calls use the right reference.
- The injected `clock` parameter is used consistently; no hidden `time.time()` calls.

### Verdict

Zero real issues found in the three targeted categories. The implementation is sound.
