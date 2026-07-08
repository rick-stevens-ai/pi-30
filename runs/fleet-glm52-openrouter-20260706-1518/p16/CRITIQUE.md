NO_ISSUES

counter.py review (data races / missing lock on shared counter only):

- `_n` is a plain int accessed only under `self._lock`.
- `incr()`: read-modify-write (`self._n = self._n + 1`) is fully enclosed in `with self._lock:`, making the RMW atomic w.r.t. other critical sections.
- `value()`: read of `_n` is also under `with self._lock:`, so it cannot observe a torn/half-applied write and serializes with `incr()`.
- `__init__` writes `_n` and `_lock` without acquiring the lock, but this runs during construction before the instance is published to any thread, so no concurrent access is possible at that point (safe publication of the fully-constructed object is the caller's responsibility, not a lock defect in this class).
- No other method or thread mutates `_n`, and the same lock guards every access. No read path bypasses the lock.

No data races or missing-lock defects found.
