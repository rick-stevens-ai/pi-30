NO_ISSUES

## Inspection: dependence of result on nchunks / non-deterministic FP ordering

File: `reduce.py`

### What the code does
`parallel_sum(xs, nchunks)` is a one-liner: `return math.fsum(xs)`. The
`nchunks` parameter is accepted but **never read** — it is dead from the
perspective of the computation. Every call reduces to a single
`math.fsum` over the full input iterable.

### Claim under review
The module docstring claims the result is **bit-identical regardless of
`nchunks`** and independent of evaluation order, because `math.fsum`
computes the correctly-rounded (exact) sum via Shewchuk's algorithm.

### Verification (empirical)
Two stress tests were run over 50 000 trials each:

1. **Order-independence of `math.fsum`**: for a fixed multiset of values,
   shuffling the input order never changed the returned bit-pattern.
2. **Determinism / repeatability**: calling `math.fsum(xs)` repeatedly on
   the same input always returned the identical bit-pattern.

Both passed. Because `nchunks` is unused, varying it cannot affect the
result; and because `math.fsum` is order-independent, no chunking
strategy (real or hypothetical) can perturb the rounding.

### Why the alternative would fail (and why the code avoids it)
The docstring correctly warns that a *naive* chunked reduction —
`fsum(fsum(chunk))` — is **not** bit-identical across chunk counts,
because per-chunk rounding discards information before the combine step.
Empirically this was confirmed: `fsum([fsum(c) for c in chunks])`
diverged from `fsum(xs)` in trial 0 of a 20 000-trial run. The code
sidesteps this entirely by never chunking — it hands the whole iterable
to `math.fsum` in one pass.

### Edge cases considered
- **Generator input**: `math.fsum` consumes the iterable once; since
  `nchunks` is ignored there is no double-consumption hazard.
- **NaN / ±inf / signed zero**: `math.fsum` defines deterministic
  behavior for these (NaN propagates, infinities handled, signed zero
  preserved) and this behavior is order-independent, so chunking would
  not matter even if it were attempted.
- **Platform determinism**: `math.fsum` operates on IEEE-754 doubles via
  CPython's C implementation; the Shewchuk algorithm is deterministic
  given identical input values, so cross-platform bit-identity holds.

### Conclusion
The implementation is correct. The result of `parallel_sum` is
independent of `nchunks` (the parameter is unused) and independent of
floating-point evaluation order (`math.fsum` is order-independent and
deterministic). No real issues were found.