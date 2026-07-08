# Token bucket rate limiter with time-based refill.
# Starts with 'capacity' tokens, refills at 'rate' tokens/sec.
class RateLimiter:
    def __init__(self, rate, per, clock):
        self.rate = rate          # tokens per period
        self.per = per            # time period in seconds
        self.clock = clock        # injected clock function
        self.capacity = rate      # max burst = rate tokens
        self.tokens = self.capacity  # start full
        self.last_time = clock()  # last check time

    def _refill(self):
        now = self.clock()
        elapsed = now - self.last_time
        self.last_time = now
        # Refill at rate tokens/sec, up to capacity
        refill_amount = self.rate * elapsed / self.per
        self.tokens = min(self.capacity, self.tokens + refill_amount)
        # Round to avoid floating-point drift
        self.tokens = round(self.tokens, 10)

    def allow(self, n=1):
        self._refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False