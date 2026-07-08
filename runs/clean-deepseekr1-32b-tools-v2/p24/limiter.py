from datetime import datetime
import math
class TokenBucket:
    def __init__(self, rate: float, capacity: int, clock=None):
        # Ensure capacity is a positive integer
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError('Capacity must be a positive integer')
        self.rate = rate
        self.capacity = capacity
        # Initialize tokens according to the injected clock function
        if clock:
            self.clock = clock
        else:
            # Use deterministic clock by default
            import time
            self.clock = lambda: math.ceil(time.time())
        self.tokens = 0.0
        self.last_refill_time = self.clock()


    def refill(self):
        now = self.clock()
        delta_seconds = now - self.last_refill_time
        if delta_seconds <= 0:
            # Prevent negative or zero deltas from adding tokens
            return
        # Calculate possible new tokens
        added_tokens = delta_seconds * self.rate
        # Add tokens without exceeding capacity
        potential_new_tokens = min(
            self.capacity,
            self.tokens + added_tokens
        )
        if potential_new_tokens != self.tokens:
            print(f'Refilling to {potential_new_tokens:.2f} tokens')
            self.tokens = potential_new_tokens
        self.last_refill_time = now

    def allow(self, n=1) -> bool:
        # Refill first to get fresh tokens
        self.refill()
        # Check if tokens after refill are available
        allowed = False
        if self.tokens >= n:
            # Subtract and ensure not negative
            new_tokens = max(0.0, self.tokens - n)
            potential_token_count = min(new_tokens, self.capacity)  # This is just to show the correct count after refill
            print(f'Allowing {n} tokens: from {self.tokens + n:.2f} to {max(potential_token_count, 0.0):.2f}')
            allowed = True
        return allowed