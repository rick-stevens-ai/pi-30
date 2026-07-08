# P16 FIXED: thread-safe counter using threading.Lock around the increment.
import threading

class SafeCounter:
    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def incr(self):
        with self._lock:
            self._n = self._n + 1

    def value(self):
        with self._lock:
            return self._n