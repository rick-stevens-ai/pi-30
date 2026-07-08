class TokenBucket:
    def __init__(self, rate, capacity, clock):
        """
        rate: tokens per second
        capacity: maximum burst size
        clock: object with __call__ returning seconds
        """
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        self.tokens = float(capacity)
        self.last_update = self.clock()

    def allow(self, n=1):
        """
        returns True if n tokens can be consumed, otherwise False.
        """
        now = self.clock()
        elapsed = now - self.last_update
        
        if elapsed > 0:
            # Refill
            new_tokens = elapsed * self.rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_update = now

        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        # Based on verify.py, capacity seems to be rate * per
        # because 5/1s -> 5 burst.
        super().__init__(rate=rate, capacity=rate * per, clock=clock)
