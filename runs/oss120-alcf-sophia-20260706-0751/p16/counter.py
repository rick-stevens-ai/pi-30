# P16 SEED: unsynchronized counter. The += is a read-modify-write that races
# under the GIL-release boundaries / bytecode interleaving at high contention,
# so the final count is < expected. Loop (driven by hostile critic) must add a
# threading.Lock around incr (or use itertools/atomic pattern).
# The implementation below provides a thread‑safe counter using a `threading.Lock`.
# The original `SafeCounter` class is retained for backward compatibility with the existing test harness (`verify.py`).
# A new `Counter` class is also provided that follows the requested API (`increment`).
import threading

class SafeCounter:
    """Thread‑safe counter used by the supplied test harness.

    The original seed version performed ``self._n = self._n + 1`` without any
    synchronization, which leads to lost updates under concurrent increments.
    A ``threading.Lock`` protects the critical section so that every increment
    is atomic with respect to other threads.
    """

    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def incr(self):
        """Increment the counter safely.

        The lock is held for the brief read‑modify‑write operation, ensuring
        that no two threads can interleave their updates.
        """
        with self._lock:
            self._n = self._n + 1

    def value(self):
        """Return the current count.

        The lock is also used when reading to guarantee a consistent view of
        the value even if other threads are concurrently updating it.
        """
        with self._lock:
            return self._n

class Counter:
    """Public API expected by the problem description.

    Provides an ``increment`` method that forwards to the thread‑safe ``incr``
    implementation of :class:`SafeCounter`.
    """

    def __init__(self):
        self._counter = SafeCounter()

    def increment(self):
        self._counter.incr()

    def value(self):
        return self._counter.value()
