"""Thread‑safe counter implementations.

The original seed used a ``SafeCounter`` class whose ``incr`` method performed
an unsynchronised ``self._n = self._n + 1``.  Under heavy contention this leads to
lost updates because the read‑modify‑write sequence can be interleaved between
threads.

The tests (``verify.py``) import ``SafeCounter`` and expect an ``incr`` method.
Therefore we keep a thread‑safe ``SafeCounter`` implementation while also
providing a more idiomatic ``Counter`` class that exposes an ``increment`` method.
Both classes share the same internal logic based on ``threading.Lock``.
"""

import threading


class _BaseCounter:
    """Common functionality for the counter implementations.

    This private base class stores the integer value and a ``Lock`` protecting
    all modifications and reads.
    """

    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def _inc(self):
        """Increment the counter while holding the lock.

        Sub‑classes expose this behaviour under different method names.
        """
        with self._lock:
            self._n += 1

    def _value(self):
        """Return the current count in a thread‑safe manner."""
        with self._lock:
            return self._n


class SafeCounter(_BaseCounter):
    """Legacy API expected by the test suite.

    Provides ``incr`` and ``value`` methods that are safe for concurrent use.
    """

    def incr(self):
        """Increment the counter (thread‑safe)."""
        self._inc()

    def value(self):
        """Return the current count (thread‑safe)."""
        return self._value()


class Counter(_BaseCounter):
    """Modern API with an ``increment`` method.

    Mirrors the behaviour of :class:`SafeCounter` but uses a more descriptive
    method name.
    """

    def increment(self):
        """Increase the counter by one (thread‑safe)."""
        self._inc()

    def value(self):
        """Return the current count (thread‑safe)."""
        return self._value()
