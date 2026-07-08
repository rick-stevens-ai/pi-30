NO_ISSUES

## Scope
Inspected `reduce.py` only, for: (a) dependence of the returned result on
`nchunks`, and (b) non-deterministic floating-point ordering.

## Verdict
No real issues found. The result is independent of `nchunks` and the FP
reduction is deterministic.

## Reasoning

1. **Single correctly-rounded reduction.** Every raw element is forwarded,
   in fixed *data* order, into exactly one `math.fsum(_chain())` call. There
   is no per-chunk rounding, no combining of partial float totals, and no
   tree of `+` operations. `nchunks` never enters the arithmetic.

2. **`nchunks` only reshapes traversal, not values/order.**
   - Sized branch: `sizes` partitions `len(xs)` into `nchunks` contiguous
     groups (`base + (i < extra)`), then a trailing `None` drains the rest.
     `_chain` yields `islice(it, size)` for each, i.e. elements 0,1,2,… in
     original order. Different `nchunks` changes only where the `islice`
     cuts happen; the stream fed to `fsum` is identical.
   - Unsized branch: `chunk = 1<<20` fixed, `sizes = [chunk]*nchunks + [None]`.
     Again the full iterable is consumed once, in order, regardless of
     `nchunks`. The comment's note that `nchunks` only sets initial
     granularity is accurate; it does not cap consumption.
   - `nchunks > total` / zero-size chunks are handled by `if size <= 0:
     continue` and the final `None` drain, so every element is still yielded
     exactly once.

3. **No non-determinism.** No threads, no RNG in the reduction path, no
   dict/hash-set used to combine numbers, no reliance on iteration order of
   an unordered container. `__main__` uses `random` only for test data, and
     sets are used only to compare results, never to compute them.

4. **fsum order-independence is not even required for the `nchunks` claim.**
   Even if one doubted that `math.fsum` is perfectly correctly-rounded, the
   stream it receives is byte-for-byte identical across `nchunks` (same
   values, same order), so the output cannot depend on `nchunks` regardless.
   The stronger claim (order-independence of `fsum`) only matters for
   cross-partition identicality, which the code does not rely on since it
   preserves data order.

## Minor non-issues (not nchunks/FP-ordering related, listed for completeness)
- The docstring asserts `math.fsum` is "correctly rounded"; CPython's
  implementation tracks exact partials and matches that in practice, but it
  is not strictly a documented guarantee. This does not affect
  `nchunks`-independence or determinism here.
- `int(nchunks)` coerces non-ints (e.g. `2.9` → 2); deterministic, just
  surprising. Irrelevant to the audit scope.
