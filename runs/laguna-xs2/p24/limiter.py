# Token bucket rate limiter: allows at most 'capacity' burst, then refills at
# 'rate' tokens/sec using the injected clock().

import math

class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate = rate
        self.capacity = capacity
        self.clock = clock
        self._tokens = float(capacity)
        self._last_update = clock()

    def allow(self, n=1):
        """Consume n tokens if available. Returns True if allowed, False otherwise."""
        now = self.clock()
        elapsed = now - self._last_update
        # Refill tokens based on rate * elapsed time
        self._tokens = min(self.capacity, self._tokens + self.rate * elapsed)
        self._last_update = now
        # Use small epsilon for floating-point comparison
        if self._tokens >= n - 1e-9:
            self._tokens -= n
            return True
        return False


# RateLimiter with (rate, per, clock) signature for backwards compatibility
class RateLimiter:
    def __init__(self, rate, per, clock):
        # rate tokens per 'per' seconds => rate/per tokens/sec
        self._bucket = TokenBucket(rate / per, rate, clock)

    def allow(self, n=1):
        return self._bucket.allow(n)


# Alias
TokenBucketRateLimiter = TokenBucket