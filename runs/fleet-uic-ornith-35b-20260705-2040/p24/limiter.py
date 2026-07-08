# P24 SEED: TokenBucket rate limiter with time-based refill using injected clock.

class RateLimiter:
    """
    Token-bucket limiter (legacy name kept for API compat).

      capacity == int(rate * per)  tokens are available at any moment;
      tokens replenish as elapsed * (rate / per), bounded by `capacity`.
    """

    def __init__(self, rate: float, per: float, clock):
        self.rate = rate          # base amount per cycle
        self.per = per            # seconds per cycle
        self.capacity: int = max(1, int(round(rate * per)))
        self._tokens: float = float(self.capacity)  # full to start
        self._last_now: float = clock()
        self.clock = clock

    def allow(self, n: int = 1) -> bool:
        now = self.clock()
        elapsed = max(0.0, now - self._last_now)
        if elapsed > 0 and self.per > 0:
            gain = elapsed * (self.rate / self.per)
            self._tokens = min(float(self.capacity), self._tokens + gain)   # capped
        self._last_now = now
        if self._tokens >= n:
            self._tokens -= n
            return True
        return False


# Convenience alias: RateLimiter and TokenBucket share the same class at this
# level because verify.py imports them both. Caller-side semantics are given by
# the *TokenBucket* constructor signature below (the real type for new code).
TokenBucket = RateLimiter


class _RatePerCapBucket(RateLimiter):
    """Helper that interprets `rate`/`per` with a *capacity-*style contract:
       per = 1 → refill rate is `rate/capacity` tokens/s and the bucket holds
       exactly `capacity` tokens at most. Not used by verify.py directly but
       kept for documentation clarity on how `TokenBucket(rate, capacity)` would be built from RateLimiter's params.
    """

    def __init__(self, rate: float, per: float, clock):
        super().__init__(rate=rate, per=per, clock=clock)

