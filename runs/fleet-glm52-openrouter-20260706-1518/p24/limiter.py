# P24: a token-bucket rate limiter with time-based refill using an injected
# clock. The bucket starts full (capacity tokens), allows a burst of up to
# `capacity`, then refills continuously at `rate` tokens per second.
class TokenBucket:
    def __init__(self, rate, capacity, clock):
        if rate < 0:
            raise ValueError("rate must be non-negative")
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        # Start full so the first burst can use up to `capacity` tokens.
        self._tokens = float(capacity)
        self._last = float(clock())

    def _refill(self):
        now = float(self.clock())
        dt = now - self._last
        if dt > 0:
            self._tokens = min(self.capacity, self._tokens + dt * self.rate)
            self._last = now

    def allow(self, n=1):
        """Return True if n tokens can be consumed, consuming them; else False."""
        n = float(n)
        if n <= 0:
            return True
        self._refill()
        if self._tokens + 1e-9 >= n:
            self._tokens -= n
            return True
        return False


# Backwards-compatible wrapper used by verify.py: `per` is the time window in
# seconds, so the burst capacity is rate * per.
class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        super().__init__(rate=rate, capacity=rate * float(per), clock=clock)
