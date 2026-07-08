class RateLimiter:
    def __init__(self, rate, per, clock):
        self.rate = rate            # tokens per second
        self.capacity = rate * per  # max burst size (tokens at t=0)
        self.clock = clock
        self.tokens = self.capacity
        self.last_time = clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = now - self.last_time
        if elapsed > 0:
            refill = elapsed * self.rate
            self.tokens += refill
            self.tokens = min(self.tokens, self.capacity)
            self.last_time = now
        # Use epsilon tolerance to avoid floating-point boundary issues
        if self.tokens >= n - 1e-9:
            self.tokens -= n
            return True
        return False
