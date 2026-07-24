# P16 SEED: unsynchronized counter. The += is a read-modify-write that races
# under the GIL-release boundaries / bytecode interleaving at high contention,
# so the final count is < expected. Loop (driven by hostile critic) must add a
# threading.Lock around incr (or use itertools/atomic pattern).
import threading


class SafeCounter:
    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def incr(self):
        # Acquire the lock around the read-modify-write so concurrent threads
        # cannot interleave between the LOAD / BINARY_ADD / STORE bytecodes.
        with self._lock:
            self._n = self._n + 1

    def value(self):
        # Acquire the same lock to return a consistent snapshot and establish a
        # happens-before relationship with the most recent locked write.
        with self._lock:
            return self._n