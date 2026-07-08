CRITIQUE.md

Found issues in limiter.py:

1. Clock misuse: When the injected clock returns a value that is less than the previous value (non-monotonic), the code sets elapsed = 0 but fails to update `self.last_update`. This causes the token bucket to stop refilling until the clock advances past the stored `self.last_update`. The fix is to update `self.last_update` to the current clock value even when elapsed is negative (or treat as zero and still advance the last update).