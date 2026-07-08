# P24 SEED: token‑bucket rate limiter (fixed). Implements a token bucket that
# allows bursts up to a fixed capacity and refills at a controlled rate using
# an injected clock function.  The class can be instantiated as either
# `TokenBucket(rate, capacity, clock)` or, for backward compatibility, as
# `RateLimiter(rate, per, clock)`.



class TokenBucket:
    """Simple token‑bucket rate limiter.

    Parameters
    ----------
    rate : float
        Tokens refilled per second.
    capacity : float
        Maximum burst capacity (number of tokens held when bucket is full).
    clock : callable
        Function that returns the current time in seconds.
    """
    def __init__(self, rate, capacity, clock):
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.clock = clock
        self.tokens = self.capacity
        # The last time is stored after the first refilling step
        self.last_time = clock()

    def allow(self, n=1):
        """Return True if *n* tokens can be consumed immediately.

        Tokens are refilled since the last call according to *rate* and the
        elapsed time since :pyattr:`self.last_time`. The bucket will never
        exceed :pyattr:`self.capacity`.
        """
        now = self.clock()
        elapsed = now - self.last_time
        if elapsed > 0:
            # Refill tokens, capped by capacity.
            new_tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.tokens = new_tokens
            self.last_time = now
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

# Backward compatibility: RateLimiter(rate, per, clock) maps to
# TokenBucket(rate / per, rate, clock)
class RateLimiter:
    """Deprecated wrapper complying with the original interface.

    Parameters
    ----------
    rate : float
        Number of events allowed per *per* seconds.
    per : float
        Time window in seconds.
    clock : callable
        Clock function that returns floating point seconds.
    """
    def __init__(self, rate, per, clock):
        # Interpret ``rate``/``per`` as tokens per second, with capacity equal
        # to the burst rate.
        tokens_per_second = float(rate) / float(per)
        capacity = float(rate)
        self._bucket = TokenBucket(tokens_per_second, capacity, clock)

    def allow(self, n=1):
        return self._bucket.allow(n)
