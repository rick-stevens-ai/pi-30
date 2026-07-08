# P16 SEED: unsynchronized counter. The += is a read-modify-write that races
# under the GIL-release boundaries / bytecode interleaving at high contention,
# so the final count is < expected. Loop (driven by hostile critic) must add a
# threading.Lock around incr (or use itertools/atomic pattern).
import threading

class SafeCounter:
    def __init__(self):
        self._lock = threading.Lock()
        self._n = 0

    def incr(self):
        with self._lock:
            self._n += 1   # Now atomic

    def def value(self):
        with self._lock:
            return self._n
