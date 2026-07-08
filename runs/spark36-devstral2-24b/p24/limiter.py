# P24 SEED: a broken limiter that always allows (no accounting). Loop (driven by
# the hostile critic) must implement a proper token bucket with time-based refill
# using the injected clock.
class RateLimiter:
    def __init__(self, rate, per, clock):
        self.rate = float(rate)
        self.period = float(per)  # time period in seconds (1/rate to get capacity?)
        self.clock = clock
        # Capacity is determined by the burst we want - since we have rate=5/s 
        # and want to allow exactly 5 at t=0, capacity should be rate * min_period
        # But actually, for a proper token bucket, capacity should be the same as max rate
        # Let me think differently: if rate is 5 per second and period is undefined,
        # we need capacity = rate to allow bursts of full rate, then refill at that rate.
        self.capacity = float(rate)  # burst capacity equals maximum rate (tokens)
        self.clock = clock
        self.tokens = self.capacity  # current available tokens
        self.last_update_time = None  # when we last updated tokens
    
    def allow(self):
        return self.allow_n(1)  # default n=1 for backward compatibility
    
    def allow_n(self, n=1):
        if not isinstance(n, (int, float)) or n <= 0:
            raise ValueError("n must be positive")
        
        current_time = self.clock()
        
        # Initialize last_update_time on first call
        if self.last_update_time is None:
            self.last_update_time = current_time
            return n <= self.tokens
        
        # Calculate time elapsed and refill tokens
        time_elapsed = current_time - self.last_update_time
        tokens_to_add = self.rate * time_elapsed
        if tokens_to_add > 0:
            self.tokens = min(self.tokens + tokens_to_add, self.capacity)
        
        self.last_update_time = current_time
        
        # Check if we have enough tokens for n requests
        result = self.tokens >= float(n)
        if result:
            self.tokens -= float(n)
        return result

class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = float(rate)  # tokens per second
        self.capacity = float(capacity)  # maximum burst size
        self.clock = clock
        self.tokens = self.capacity  # current available tokens
        self.last_update_time = None  # when we last updated tokens
    
    def allow(self, n=1):
        if not isinstance(n, (int, float)) or n <= 0:
            raise ValueError("n must be positive")
        
        current_time = self.clock()
        
        # Initialize last_update_time on first call
        if self.last_update_time is None:
            self.last_update_time = current_time
            return n <= self.tokens
        
        # Calculate time elapsed and refill tokens
        time_elapsed = current_time - self.last_update_time
        tokens_to_add = self.rate * time_elapsed
        if tokens_to_add > 0:
            self.tokens = min(self.tokens + tokens_to_add, self.capacity)
        
        self.last_update_time = current_time
        
        # Check if we have enough tokens for n requests
        result = self.tokens >= float(n)
        if result:
            self.tokens -= float(n)
        return result