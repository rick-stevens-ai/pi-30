# Critical Findings

1. **No accounting or token bucket logic** – The `RateLimiter` class simply returns `True` from `allow()` for every call, effectively disabling any rate limiting.

2. **Missing state for tokens** – There is no storage for the current token count, nor a capacity or last‑refill timestamp. Without this state์ the bucket can never enforce a burst threshold.

3. **No capacity/variance handling** – The constructor accepts `rate` and `per` (presumably to compute tokens per interval), but these are never used, so burst limits or refill schedules are never applied.

4. **Clock is unused** – The injected `clock` parameter is not referenced anywhere. A proper implementation should use it to compute elapsed time between refills.

5. **Refill math is absent** – Because the code never calculates how many tokens to add based on elapsed time, it cannot correctly simulate a token bucket’s *time‑based* refill mechanism.

6. **Burst‑exceeds‑capacity logic missing** – There is no check against a maximum burst size; the code will never reject calls even if a burst would exceed the allowed capacity.

7. **Potential shall‑do concurrency issues** – Even if the code were fixed, accessing and updating a shared state without synchronization could lead to race conditions in a multi‑threaded environment.

---

> **Implication** – As written, the limiter cannot enforce any limit, rendering any rate‑limiting feature ineffective. The library would need substantial changes to correctly implement a token‑bucket algorithm, including state, refill logic, and capacity handling.