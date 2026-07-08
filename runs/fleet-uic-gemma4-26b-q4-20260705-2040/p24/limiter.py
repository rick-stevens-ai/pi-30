class TokenBucket:
    def __init__(self, rate, capacity, clock):
        """
        :param rate: tokens per second to refill
        :param capacity: maximum number of tokens in the bucket (burst)
        :param clock: a callable that returns the current time in seconds
        """
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        self.tokens = float(capacity)
        self.last_time = self.clock()

    def allow(self, n=1):
        """
        :param n: number of tokens to consume
        :return: True if tokens were available and consumed, False otherwise
        """
        now = self.clock()
        delta = now - self.last_time
        if delta > 0:
            self.tokens = min(self.capacity, self.tokens + delta * self.rate)
            self.last_time = now
        
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        # Convert 'rate' events per 'per' seconds to tokens/sec and capacity
        super().__init__(rate=rate/per, capacity=rate, clock=clock)

    def allow(self, n=1):
        return super().allow(n)
