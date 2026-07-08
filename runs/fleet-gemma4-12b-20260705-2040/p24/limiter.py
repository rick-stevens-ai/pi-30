class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self.tokens = float(capacity)
        self.last_update = self.clock()

    def allow(self, n=1):
        now = self.clock()
        elapsed = max(0, now - self.last_update)
        refill = elapsed * self.rate
        
        if refill > 0:
            # If the refill would exceed capacity, we only move last_update by 
            # the amount of time needed to reach capacity.
            if self.tokens + refill > self.capacity:
                time_to_reach_cap = (self.capacity - self.tokens) / self.rate
                self.last_update += time_to_reach_cap
                self.tokens = float(self.capacity)
            else:
                # To address the precision loss critique, we only update 
                # last_update if the refill actually changed the token count.
                new_tokens = self.tokens + refill
                if new_tokens > self.tokens:
                    self.tokens = new_tokens
                    self.last_update = now
        
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

class RateLimiter:
    def __init__(self, rate, per, clock):
        # For RateLimiter(rate=5, per=1.0), 
        # capacity is 'rate' (5)
        # refill rate is 'rate / per' (5/1.0 = 5 tokens/sec)
        self.bucket = TokenBucket(rate / per, rate, clock)

    def allow(self):
        return self.bucket.allow(1)
