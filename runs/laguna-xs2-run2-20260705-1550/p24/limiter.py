# P24: Token Bucket Rate Limiter
# Allows at most 'capacity' burst, then refills at 'rate' tokens/sec using injected clock()

_EPS = 1e-9

class TokenBucket:
    """Token bucket rate limiter.
    
    Args:
        rate: Tokens added per second
        capacity: Maximum burst (starting token count)
        clock: Callable returning current time
    """
    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self._tokens = float(capacity)
        self._last_update = None
    
    def allow(self, n=1):
        """Attempt to consume n tokens. Returns True if allowed, False otherwise."""
        now = self.clock()
        
        # First call: initialize timestamp
        if self._last_update is None:
            self._last_update = now
            if self._tokens >= n - _EPS:
                self._tokens -= n
                return True
            return False
        
        # Refill tokens based on elapsed time
        elapsed = now - self._last_update
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._last_update = now
        
        # Attempt to consume tokens (with epsilon for floating point)
        if self._tokens >= n - _EPS:
            self._tokens -= n
            return True
        return False


# Alias for compatibility with verify.py interface
# RateLimiter(rate, per, clock) where per is the time window
class RateLimiter(TokenBucket):
    def __init__(self, rate, per, clock):
        # per is the time window, so capacity = rate tokens per per seconds
        super().__init__(rate=rate/per, capacity=rate, clock=clock)