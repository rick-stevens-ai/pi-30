# Token bucket rate limiter implementation.
# The limiter allows at most ``capacity`` events in an instantaneous burst
# and refills continuously at ``rate`` tokens per second using the injected
# ``clock`` callable.

class TokenBucket:
    """A classic token‑bucket limiter.

    Parameters
    ----------
    rate: float
        Number of tokens added to the bucket each second.
    capacity: float
        Maximum number of tokens that can accumulate – the burst size.
    clock: callable
        Function returning the current monotonic time in seconds.
    """

    def __init__(self, rate, capacity, clock):
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        # start full so an initial burst up to ``capacity`` is allowed
        self._tokens = self.capacity
        self._last = self.clock()

    def _refill(self):
        """Replenish tokens based on elapsed time since the last call."""
        now = self.clock()
        elapsed = now - self._last
        if elapsed > 0:
            # Add tokens proportionally, but never exceed the bucket capacity.
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last = now

    def allow(self, n: int = 1) -> bool:
        """Consume ``n`` tokens if enough are available.

        Returns ``True`` and deducts the tokens when the bucket has at least
        ``n`` tokens; otherwise returns ``False`` and leaves the bucket unchanged.
        """
        if n <= 0:
            return True
        self._refill()
        # Slight tolerance for floating‑point rounding errors.
        if self._tokens + 1e-9 >= n:
            self._tokens -= n
            return True
        return False


# ---------------------------------------------------------------------------
# Compatibility layer
# ---------------------------------------------------------------------------
class RateLimiter:
    """Legacy wrapper preserving the original ``RateLimiter`` API.

    The original tests instantiate ``RateLimiter(rate, per, clock)`` where
    ``capacity = rate * per``.  Internally this class delegates to
    :class:`TokenBucket` to provide the correct bursting and refill behaviour.
    """

    def __init__(self, rate, per, clock):
        # ``per`` specifies the time window for the burst; the effective burst
        # size is ``rate * per`` tokens.
        capacity = float(rate) * float(per)
        self._bucket = TokenBucket(rate, capacity, clock)

    def allow(self, n: int = 1) -> bool:
        return self._bucket.allow(n)
