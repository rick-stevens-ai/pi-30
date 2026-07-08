# P24 SEED: a broken limiter that always allows (no accounting). Loop (driven by
# the hostile critic) must implement a proper token bucket with time-based refill
# using the injected clock. 

class TokenBucket:
    """Token bucket that permits up to `capacity` burst tokens and then refills at `rate` tokens per second."""
    
    def __init__(self, rate: float, capacity: int, clock):
        self.rate = max(0.0, rate)
        self.capacity = max(0, int(capacity))
        self.clock = clock
        # Start with a full bucket so the first `capacity` calls are allowed immediately.
        self._tokens = float(self.capacity)
        self._last_timestamp = clock()

    def _refill(self):
        now = self.clock()
        elapsed = now - self._last_timestamp
        if elapsed > 0:
            added = min(self.rate * elapsed, self.capacity - self._tokens)
            self._tokens += added
            self._last_timestamp = now

    def allow(self, n: float = 1):
        """Allow `n` tokens to be consumed; returns True on success."""
        self._refill()
        if n <= self._tokens:
            self._tokens -= float(n)
            return True
        else:
            return False