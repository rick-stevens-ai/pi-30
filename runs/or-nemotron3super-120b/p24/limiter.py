# P24 SEED: a broken limiter that always allows (no accounting). Loop (driven by
# the hostile critic) must implement a proper token bucket with time-based refill
# using the injected clock.
class RateLimiter:
    def __init__(self, rate, per, clock):
        self.rate = rate          # tokens per second
        self.per = per            # seconds per rate period (capacity = rate * per)
        self.clock = clock        # callable returning current time (seconds)
        self.capacity = rate * per  # maximum tokens in bucket
        self.tokens = self.capacity   # start with a full bucket
        self.last_update = self.clock()  # time of last token update

    def allow(self, n=1):
        if n <= 0:
            return True
        now = self.clock()
        elapsed = now - self.last_update
        # Guard against non-monotonic clock
        if elapsed < 0.0:
            elapsed = 0.0
        self.last_update = now
        # Refill tokens based on elapsed time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        # Allow if we have enough tokens (with small tolerance to counter rounding down)
        # but also ensure we do not exceed capacity
        epsilon = 1e-9
        if n > self.capacity + epsilon:
            return False
        if self.tokens >= n - epsilon:
            self.tokens -= n
            # Ensure tokens don't go negative due to rounding
            if self.tokens < 0:
                self.tokens = 0.0
            return True
        return False