# Limiter.py Code Critique

## Critical Defects Found (3)

1. **Burst Exceeding Capacity**: The `allow()` method always returns True, completely bypassing capacity enforcement with no internal state for monitoring consumption.

2. **Wrong Refill Math/No Accounting Actually Implemented - Not Wrong: There's No State Tracking At All**:
   * Tokens are never decremented on successful allows
   * Bucket level (state) is not tracked between calls

3. **Clock Misuse**: The injected `clock` parameter from constructor (`self.clock`) is accepted but NEVER used anywhere in the class logic.

## Summary:

This implementation completely fails to implement a token bucket algorithm:
* No internal state for tokens, capacity or last_update_timestamp
* Allow() always returns True without any checking against rate/per/clock values passed during construction

The file appears intentionally broken (comments acknowledge this) but functionally represents all three failure modes listed.