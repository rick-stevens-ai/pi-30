## CRITIQUE of limiter.py

### 1. `_RatePerCapBucket` subclass has a broken / self-contradicting contract

The class is documented as interpreting `rate/capacity` tokens/s with the *capacity* argument:
```
Not used by verify.py directly but kept for documentation clarity on how
`TokenBucket(rate, capacity)` would be built from RateLimiter's params.
```

Yet its actual constructor signature is `(self, rate: float, per: float, clock)` — it takes **no `capacity` argument at all**, and forwards both positional args straight to the parent's `(rate=rate, per=per, clock=clock)`. Two problems result:

- Any caller that tries to use the documented pattern `TokenBucket(rate, capacity)` will silently pass `capacity` as `per` — e.g. a **low `capacity` value of 3** becomes an absurdly fast refill period of 0s → `rate / per` blows up and the limiter never denies anything.
- The docstring claims that when `per == 1`, "refill rate is `rate/capacity` tokens/s" — but nothing in code ever forces or checks `self.per == 1`. A caller passing e.g. `per=5` produces a refill and capacity consistent with the **parent's** rounding rule, not with the claimed contract.

The whole subclass is an *inverted* documentation hazard: it asserts what it does *but its implementation disagrees*. Even if verify.py doesn't call it directly, any other consumer picking up `TokenBucket = RateLimiter` plus `_RatePerCapBucket(RateLimiter)` will follow that docstring and misuse the API.

#### Severity
The class is "not used by verify.py" so there are **no test failures** — meaning the documentation-only hazard can hide behind "dead code / not exercised" for an arbitrary amount of time until a real consumer tries it (or `verify.py` gains that feature later, at which point this silently breaks).

Practically: in this repo at this moment, removing or correcting the subclass is required if the docstring's stated contract is the intended behavior. As written it does neither the documented thing nor something usefully different from its parent.
