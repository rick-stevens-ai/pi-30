class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = float(capacity)
        self.last = clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = now - self.last
        self.tokens = min(self.capacity, self.tokens + self.rate * elapsed)
        self.last = now
        if self.tokens >= n - 1e-9:
            self.tokens -= n
            return True
        return False

# alias for compatibility with verify.py
class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        capacity = rate * per
        super().__init__(rate, capacity, clock)
    # allow inherited
