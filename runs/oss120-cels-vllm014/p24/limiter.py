"""Token‑bucket rate limiter.

The original implementation exposed two classes:
* ``RateLimiter(rate, per, clock)`` – tokens are added at ``rate/per``
  tokens per second and the bucket capacity is ``rate``.
* ``TokenBucket(rate, capacity, clock)`` – a thin wrapper required by the
  problem statement. It must allow at most ``capacity`` events instantly
  (a burst) and then refill at ``rate`` tokens per second.

Both classes share the same core logic: on each ``allow`` call we first
recalculate the current token count based on the elapsed time reported by
the injected ``clock``.  Tokens never exceed the configured capacity.  The
method ``allow(n=1)`` returns ``True`` only when at least ``n`` tokens are
available; otherwise it returns ``False`` and leaves the bucket unchanged.

The implementation below keeps ``RateLimiter`` (used by the provided test
suite) and provides a clean ``TokenBucket`` wrapper that forwards to it.
"""

class RateLimiter:
    """Core token‑bucket implementation.

    Parameters
    ----------
    rate: float
        Number of tokens added per ``per`` seconds.
    per: float
        Length of the refill interval in seconds.
    clock: Callable[[], float]
        Function returning the current time in seconds.
    """

    def __init__(self, rate, per, clock):
        # The maximum number of tokens that can be stored.
        self.capacity = float(rate)
        # Start full.
        self.tokens = self.capacity
        # Refill rate measured in tokens per second.
        self.refill_rate = float(rate) / float(per) if per != 0 else 0.0
        self.clock = clock
        # Record the time of the last refill.
        self.last_timestamp = self.clock()

    def _refill(self):
        """Update ``self.tokens`` based on the time elapsed since the last call.
        The token count is clamped to ``self.capacity``.
        """
        now = self.clock()
        elapsed = now - self.last_timestamp
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_timestamp = now

    def allow(self, n: int = 1) -> bool:
        """Consume ``n`` tokens if enough are available.

        Returns ``True`` when the bucket contained at least ``n`` tokens;
        otherwise ``False``.  ``n`` may be any positive integer; ``n <= 0``
        is treated as a no‑op and returns ``True``.
        """
        if n <= 0:
            return True
        self._refill()
        # Small epsilon protects against floating‑point rounding errors.
        if self.tokens + 1e-9 >= n:
            self.tokens -= n
            # Clamp to zero to avoid tiny negative values.
            if self.tokens < 0:
                self.tokens = 0.0
            return True
        return False


class TokenBucket:
    """Public API required by the problem statement.

    ``TokenBucket(rate, capacity, clock)`` behaves like a standard token bucket
    where ``rate`` tokens are added each second and the bucket can hold up to
    ``capacity`` tokens (the burst size).  Internally it re‑uses ``RateLimiter``
    with a ``per`` of ``1`` second.
    """

    def __init__(self, rate, capacity, clock):
        # Reuse the core implementation; ``per``=1 second.
        self._rl = RateLimiter(rate, 1.0, clock)
        # Apply the requested burst capacity.
        self._rl.capacity = float(capacity)
        self._rl.tokens = float(capacity)  # start full

    def allow(self, n: int = 1) -> bool:
        """Consume ``n`` tokens if available, delegating to the underlying limiter."""
        return self._rl.allow(n)

