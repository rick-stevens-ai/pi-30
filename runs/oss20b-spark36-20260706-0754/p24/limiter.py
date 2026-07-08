# Token‑bucket rate limiter implementation.
#
# The class can be instantiated as either
#   TokenBucket(rate, capacity, clock)
# or (for backward compatibility) with a ``per`` keyword argument instead of
# capacity.  In that case the burst size is derived as
#   ceil(rate * per), but never less than 1.
#
# The public API mirrors the original challenge: a ``allow(n=1) -> bool``
# method and an attribute ``tokens`` which tracks the current token count.
# A small epsilon (1e‑12) is used when comparing floating point values to
# mitigate edge cases caused by binary representation errors.

import math
from typing import Callable

__all__ = ["TokenBucket", "RateLimiter"]


class TokenBucket:
    """Token‑bucket style rate limiter.

    Parameters
    ----------
    rate : float
        Tokens produced per second.
    capacity : int | float | None, optional
        Maximum burst size.  If ``None`` and a ``per`` keyword is supplied,
        this value is derived as :math:`\lceil\text{rate} \times \,\text{per}\rceil`
        with a minimum of one.
    clock : Callable[[], float]
        Zero‑argument callable that returns the current time in seconds.

    If ``capacity`` is omitted but ``per`` is supplied, the constructor
    behaves like ``TokenBucket(rate, math.ceil(rate * per, 1))``.  This keeps
    backwards compatibility with the original ``RateLimiter``
    implementation used in test harnesses.
    """

    def __init__(self, rate: float, capacity=None, clock: Callable[[], float] = None, *, per: float | None = None):
        self.rate = float(rate)

        # Determine burst capacity.
        if capacity is None:
            if per is None:
                raise TypeError("Missing required argument 'capacity' or keyword 'per'")
            # Ensure at least one token can be stored.
            self.capacity = max(1, int(math.ceil(self.rate * per)))
        else:
            # ``capacity`` may come as an integer or a float; store as float to
            # allow fractional consumption where appropriate.
            # Ensure capacity is a positive integer value.
            self.capacity = int(math.ceil(float(capacity)))

        if clock is None:
            raise TypeError("Missing required argument 'clock'")
        self.clock = clock

        # Current token count starts full.
        self.tokens: float = float(self.capacity)
        # Initialise the last update time to now.
        self._last_time: float = self.clock()

    def _refill(self) -> None:
        """Accumulate tokens based on elapsed time since the last check."""
        now = self.clock()
        elapsed = now - self._last_time
        if elapsed > 0:
            added = elapsed * self.rate
            # The bucket may hold at most ``capacity`` tokens.
            self.tokens = min(self.capacity, self.tokens + added)
            self._last_time = now

    def allow(self, n: int = 1) -> bool:
        """Return ``True`` if at least ``n`` tokens are available.

        Calling :meth:`allow` consumes the tokens; otherwise returns
        ``False`` without changing state. The bucket does not accumulate
        fractional portions beyond the capacity.
        """
        self._refill()
        if n <= 0:
            return True
        # Tiny epsilon guards against floating‑point noise when ``tokens`` is
        # very close to an integer boundary.
        if self.tokens >= n - 1e-12:
            self.tokens -= n
            return True
        return False

# Backwards compatibility: the original challenge used a class named
# ``RateLimiter`` that accepted ``rate``, ``per`` and ``clock``.  Defining an
# alias with the same name keeps those imports working while the new
# implementation lives in TokenBucket.
RateLimiter = TokenBucket
