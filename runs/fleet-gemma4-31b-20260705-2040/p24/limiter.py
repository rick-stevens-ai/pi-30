class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        self.tokens = self.capacity
        self.last_time = self.clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = now - self.last_time
        self.last_time = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        
        if self.tokens >= n - 1e-9:
            self.tokens -= n
            if self.tokens < 0:
                self.tokens = 0
            return True
        return False

class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        super().__init__(rate=float(rate) / float(per), capacity=float(rate), clock=clock)
