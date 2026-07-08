class TokenBucket:
    def __init__(self, rate: float, capacity: float, clock):
        """
        Initializes the TokenBucket.

        Args:
            rate: The rate at which tokens are added (tokens per second).
            capacity: The maximum number of tokens the bucket can hold.
            clock: An object providing access to the current time (e.g., clock.now() returns seconds since epoch).
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity  # Start with a full bucket for the initial burst
        self.last_refill_time = clock.now()

    def _refill(self, current_time: float):
        """Refills tokens based on the time elapsed since the last refill."""
        time_elapsed = current_time - self.last_refill_time
        if time_elapsed < 0:
            # Handle non-monotonic clock reading as suggested by critique
            raise ValueError("Clock is not monotonic; time has moved backward.")
        if time_elapsed > 0:
            tokens_to_add = time_elapsed * self.rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill_time = current_time

    def allow(self, n: float = 1.0) -> bool:
        """
        Attempts to consume 'n' tokens from the bucket. Refills tokens based on time elapsed.

        Args:
            n: The number of tokens requested. Defaults to 1.0.

        Returns:
            True if 'n' tokens were successfully consumed, False otherwise.
        """
        current_time = self.clock.now()
        self._refill(current_time)

        if self.tokens >= n:
            self.tokens -= n
            return True
        else:
            return False