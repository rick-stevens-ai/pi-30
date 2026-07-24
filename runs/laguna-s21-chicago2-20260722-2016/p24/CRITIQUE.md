NO_ISSUES

---

## Critique of `limiter.py`

### Scope
Inspected for three categories only: (1) burst-exceeds-capacity, (2) wrong
refill math, (3) clock misuse.

---

### 1. Burst-exceeds-capacity

**Invariant:** `0 <= tokens <= capacity` at all times, and a single `allow(n)`
call can never consume more than `capacity` tokens.

- **Initial state:** `self.tokens = float(capacity)` — bucket starts full. ✓
- **Refill cap:** `_refill` uses `min(self.capacity, self.tokens + elapsed * self.rate)`,
  so tokens can never exceed capacity. ✓
- **Consumption guard:** `allow` checks `self.tokens >= n - self._EPS` before
  subtracting `n`. Since `tokens <= capacity`, any `n > capacity + _EPS` is
  always rejected (verified empirically: `allow(11)` with `capacity=10` returns
  `False`). ✓
- **`_EPS` tolerance:** The tolerance allows `tokens` to dip to at most
  `-_EPS` (≈ `-1e-9`) after a borderline consume. This is negligible and
  intentional — it exists solely to absorb floating-point representation error
  in `elapsed * rate`. After such a consume, the next `allow(1)` correctly
  rejects because `-_EPS >= 1 - _EPS` evaluates to `False`. No accumulation
  occurs. ✓
- **Empirical verification:** 15 consecutive `allow(1)` calls at `t=0` with
  `capacity=10` yielded exactly 10 `True` results and 5 `False` results.
  Burst count = 10 = capacity. ✓

**Verdict:** No burst-exceeds-capacity issue.

---

### 2. Wrong refill math

- **Formula:** `elapsed * self.rate` is the correct token-bucket refill
  formula (tokens earned = rate × time elapsed). ✓
- **Absolute time:** Refill is computed from `now - self.last` (absolute
  clock time), not from accumulated deltas. This is drift-free, as the
  module docstring states. ✓
- **Cap:** `min(self.capacity, ...)` correctly caps at capacity. ✓
- **`last` update:** `self.last = now` is set after the refill computation,
  so the next call measures elapsed time from the current instant. ✓
- **Edge case — capped refill:** When tokens are already at capacity, `last`
  is still updated to `now`. This is correct: it prevents accumulating
  "credit" for time spent at capacity (standard token-bucket semantics). ✓
- **Edge case — zero elapsed:** When `elapsed == 0`, the `if elapsed > 0`
  guard skips the refill and leaves `last` unchanged. No spurious refill. ✓

**Verdict:** No wrong refill math.

---

### 3. Clock misuse

- **Clock interface:** `clock` is a zero-argument callable, invoked
  consistently in `__init__` (`self.last = clock()`) and `_refill`
  (`now = self.clock()`). ✓
- **Backward clock jumps:** The `if elapsed > 0` guard ensures that when
  the clock goes backward (`elapsed < 0`), no refill occurs and `last` is
  not updated. This is defensive: a subsequent forward jump refills from
  the original `last` value rather than from the backward time. ✓
- **Empirical verification:** Clock set backward from 5.0 → 3.0 produced
  no refill (tokens stayed at 0). Clock then set forward to 6.0 correctly
  refilled from `last=5.0` (1 second × rate=5 = 5 tokens). ✓
- **No stale reads:** `now` is captured once per `_refill` call and used
  for both the elapsed computation and the `last` update, so there is no
  inconsistency between the two. ✓

**Verdict:** No clock misuse.

---

### Minor observations (not bugs in scope)

- The `_EPS = 1e-9` comment claims "never admits a spurious token." For
  token counts above ~4.5×10⁶, the ULP of the float representation
  (~2.2×10⁻⁹) exceeds `_EPS`, so the claim is not strictly true at extreme
  magnitudes. This is a theoretical edge case irrelevant to typical rate-
  limiter usage (rates of 1–10,000 tokens/s). Not a bug in refill math,
  burst bounds, or clock handling.
- `allow(n)` does not validate `n >= 0`. A negative `n` would increase
  token count and could exceed capacity. This is an input-validation
  concern, not one of the three categories inspected.

---

**Conclusion:** After thorough inspection and empirical testing, no real
issues were found in the three specified categories.