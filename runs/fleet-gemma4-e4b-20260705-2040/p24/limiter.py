# P24 SEED: a broken limiter that always allows (no accounting). Loop (driven by
# the hostile critic) must implement a proper token bucket with time-based refill
# using the injected clock.

class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = rate  # Tokens per second refill rate
        self.capacity = capacity # Max tokens allowed (burst limit)
        self.clock = clock
        self.tokens = capacity
        self.last_refill_time = clock()

    def _refill(self):
        now = self.clock()
        time_elapsed = now - self.last_refill_time
        
        # Calculate tokens to add: rate * time_elapsed
        tokens_to_add = max(0.0, time_elapsed) * self.rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    def allow(self, n: int = 1) -> bool:
        self._refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False
