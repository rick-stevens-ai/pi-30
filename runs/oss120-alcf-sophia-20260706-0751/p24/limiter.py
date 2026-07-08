# P24: Token bucket rate limiter implementation.
# The limiter allows at most `capacity` bursts and refills tokens at `rate`
# tokens per second using the injected `clock` callable. The original tests
# (verify.py) instantiate the class as `RateLimiter(rate, per, clock)` where
# `rate` events are permitted per `per` seconds.  This corresponds to a bucket
# with a capacity equal to `rate` (i.e., the maximum burst size) and a refill
# rate of `rate/per` tokens per second.
#
# For flexibility we expose the implementation as `TokenBucket` with the
# signature `TokenBucket(rate, capacity, clock)`.  To retain compatibility with
# the existing tests we provide an alias `RateLimiter` that forwards to the
# same implementation, interpreting `capacity` as `rate` (the burst size) and
# computing the per‑second refill rate as `rate/per`.

import math

class TokenBucket:
    """Token bucket rate limiter.

    Parameters
    ----------
    rate: float
        Number of tokens added to the bucket per *second*.
    capacity: float
        Maximum number of tokens the bucket can hold (burst size).
    clock: Callable[[], float]
        Function returning the current time in seconds. Allows deterministic
        testing by injecting a mock clock.
    """

    def __init__(self, rate, capacity, clock):
        self._rate = float(rate)          # tokens per second
        self._capacity = float(capacity)  # max tokens
        self._clock = clock
        # Start with a full bucket so an immediate burst up to `capacity`
        # tokens is allowed.
        self._tokens = self._capacity
        self._last = self._clock()

    def _refill(self):
        """Refill tokens based on elapsed time since the last check."""
        now = self._clock()
        elapsed = now - self._last
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
            self._last = now

    def allow(self, n: int = 1) -> bool:
        """Consume *n* tokens if available.

        Returns ``True`` when the bucket had at least ``n`` tokens and they were
        deducted; otherwise returns ``False`` and leaves the bucket unchanged.
        """
        if n <= 0:
            return True
        self._refill()
        # Use the integer part of tokens for availability to avoid
        # floating‑point rounding issues (e.g., 0.9999999 < 1). The fractional
        # remainder is retained for future refills.
        # Adding a tiny epsilon mitigates floating‑point drift when the
        # token count is very close to an integer (e.g., 0.999999999).
        available = int(self._tokens + 1e-9)
        if available >= n:
            self._tokens -= n
            return True
        return False


# Compatibility shim for the original `RateLimiter` name expected by verify.py.
class RateLimiter(TokenBucket):
    """Alias compatible with the original test suite.

    The original constructor accepted ``rate`` and ``per`` arguments where
    ``rate`` events were allowed per ``per`` seconds.  This maps to a bucket
    capacity of ``rate`` and a refill rate of ``rate/per`` tokens per second.
    """

    def __init__(self, rate, per, clock):
        # Compute per‑second rate and set capacity equal to the burst size.
        refill_rate = float(rate) / float(per) if per != 0 else 0.0
        super().__init__(refill_rate, float(rate), clock)
