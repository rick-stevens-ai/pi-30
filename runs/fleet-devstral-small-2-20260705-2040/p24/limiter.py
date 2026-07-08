# P24 SEED: a broken limiter that always allows (no accounting). Loop (driven by
# the hostile critic) must implement a proper token bucket with time-based refill
# using the injected clock.
class RateLimiter:
    def __init__(self, rate, per, clock):
        self.rate = rate
        self.capacity = rate * per
        self.clock = clock
        self.tokens = self.capacity
        self.last_refill = clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now
        # Use epsilon to handle floating-point comparison issues
        if self.tokens >= n - 1e-9:
            self.tokens -= n
            return True
        return False
