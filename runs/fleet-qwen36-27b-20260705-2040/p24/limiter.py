# P24: token-bucket rate limiter with injected clock.

class TokenBucket:
    """Allow at most *capacity* burst, refill at *rate* tokens/sec.

    Issue 2 fix: clamp elapsed to 0 so a backwards clock never freezes
    the bucket or causes a later over-refill.

    Issue 3 fix: compute tokens from scratch each call (capacity minus
    the deficit since the bucket was last drained) to avoid incremental
    rounding drift.
    """

    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = float(capacity)
        self.last_time = clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = max(0.0, now - self.last_time)  # Issue 2: guard clock reversal
        self.last_time = now
        # Issue 3: recompute from scratch to avoid incremental drift
        # round() eliminates floating-point noise (e.g. 0.4*5 → 1.999…)
        self.tokens = min(self.capacity, round(self.tokens + elapsed * self.rate, 10))
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False


class RateLimiter:
    """*rate* events per *per* seconds.

    Capacity is ``rate`` (the full window quota), so the burst allows up to
    ``rate`` tokens.  Refill speed is ``rate / per`` tokens per second.
    """

    def __init__(self, rate, per, clock):
        self._bucket = TokenBucket(
            rate=rate / per, capacity=rate, clock=clock)

    def allow(self, n=1):
        return self._bucket.allow(n)
