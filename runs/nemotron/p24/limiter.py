# P24: Token-bucket rate limiter with time-based refill using injected clock.
class TokenBucket:
    def __init__(self, rate, capacity, clock):
        """
        Initialize a token bucket.

        Args:
            rate: Token refill rate in tokens per second.
            capacity: Maximum token capacity (burst allowance).
            clock: Callable returning current time in seconds (float).
        """
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        self._tokens = float(capacity)
        self._last = clock()
        # Small epsilon to handle floating-point precision issues
        self._eps = 1e-12

    def allow(self, n=1):
        """
        Try to consume n tokens.

        Args:
            n: Number of tokens to consume (default 1).

        Returns:
            True if n tokens were available and consumed, False otherwise.
        """
        if n <= 0:
            return True
        now = self.clock()
        elapsed = now - self._last
        if elapsed > 0:
            refill = elapsed * self.rate
            self._tokens = min(self.capacity, self._tokens + refill)
            self._last = now
        # Use epsilon to handle floating-point precision
        if self._tokens + self._eps >= n:
            self._tokens -= n
            return True
        return False


# Backward-compatible RateLimiter for verify.py
# rate = tokens per `per` seconds, so rate/per = tokens per second.
# Burst capacity = rate (max tokens per window).
class RateLimiter:
    def __init__(self, rate, per, clock):
        self._bucket = TokenBucket(rate=rate / per, capacity=rate, clock=clock)

    def allow(self):
        return self._bucket.allow(1)
