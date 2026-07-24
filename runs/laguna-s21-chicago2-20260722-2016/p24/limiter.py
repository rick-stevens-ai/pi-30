# P24: Token bucket rate limiter with time-based refill using an injected clock.
#
# TokenBucket(rate, capacity, clock):
#   - capacity: maximum burst size (and initial token count)
#   - rate:     refill rate in tokens/second
#   - clock:    zero-argument callable returning current time (seconds)
#   - allow(n=1) -> bool: consume n tokens if available, else reject
#
# Refill is computed from absolute clock time (now - last) rather than by
# accumulating elapsed deltas, which keeps the bookkeeping drift-free.


class TokenBucket:
    # Tolerance for floating-point comparisons in token counts.
    # Absorbs representation error from (now - last) * rate so that, e.g.,
    # 0.4s * 5 tokens/s yields a usable 2.0 rather than 1.9999999999999996,
    # which after consuming 1 token drops to 0.9999999999999996 < 1 and
    # wrongly rejects the second allow().
    _EPS = 1e-9

    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = float(capacity)  # start full => a full burst is allowed
        self.last = clock()

    def _refill(self):
        """Add tokens earned since the last call, capped at capacity."""
        now = self.clock()
        elapsed = now - self.last
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last = now

    def allow(self, n=1):
        """Return True and consume n tokens if enough are available."""
        self._refill()
        # Use a tolerance so that floating-point representation error in
        # the refill (elapsed * rate) does not cause a borderline token
        # count to be rejected.  The error is O(eps * magnitude) ~ 1e-15,
        # so _EPS = 1e-9 is a safe margin that never admits a spurious token.
        if self.tokens >= n - self._EPS:
            self.tokens -= n
            return True
        return False


# Backwards-compatible adapter used by verify.py:
#   RateLimiter(rate, per, clock)  ->  5 events per `per` seconds
# maps to a token bucket with capacity = rate*per and refill rate = rate/per.
class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        super().__init__(rate=rate / per, capacity=rate * per, clock=clock)