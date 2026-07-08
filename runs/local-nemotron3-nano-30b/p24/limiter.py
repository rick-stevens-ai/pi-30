# Token bucket implementation using injected clock for time measurements.
class TokenBucket:
    """
    A token bucket that allows bursts up to `capacity` tokens and refills at
    a steady rate of `rate` tokens per second. Uses an injected `clock`
    function (called with no arguments) to obtain the current time.

    The primary method is `allow(n=1)` which returns True if at least `n`
    tokens are available, consuming them from the bucket; otherwise it
    returns False.
    
    Requests for more than `capacity` tokens are explicitly rejected.
    """
    def __init__(self, rate, capacity, clock):
        self.rate = rate          # Refill rate in tokens per second
        self.capacity = capacity  # Maximum number of tokens (burst size)
        self.tokens = capacity    # Start full for burst allowance
        self.clock = clock        # Function returning current time (monotonic)
        self.last_update = None   # Timestamp of last call to allow

    def _refill(self):
        """Update the token count based on elapsed monotonic time."""
        if self.last_update is None:
            # First call – just record timestamp; no refill yet.
            pass
        else:
            now = self.clock()
            # Ensure we only use non‑negative elapsed time to avoid negative adds.
            elapsed = max(0.0, now - self.last_update)
            added = elapsed * self.rate
            self.tokens = min(self.capacity, self.tokens + added)
        self.last_update = self.clock()

    def allow(self, n=1):
        """
        Return True if at least `n` tokens are available, consuming them.
        Explicitly rejects non‑positive or excessively large requests
        (greater than the bucket capacity).
        """
        # Guard against invalid request sizes.
        if n <= 0 or n > self.capacity:
            return False

        self._refill()                 # Update token count based on time elapsed
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False