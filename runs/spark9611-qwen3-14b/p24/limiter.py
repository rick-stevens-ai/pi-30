class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = capacity
        self.last_refill_time = clock()

    def allow(self, n=1):
        current_time = self.clock()
        delta_time = current_time - self.last_refill_time
        tokens_to_add = delta_time * self.rate
        self.tokens = min(self.tokens + tokens_to_add, self.capacity)
        self.last_refill_time = current_time

        if self.tokens >= n:
            self.tokens -= n
            return True
        return False