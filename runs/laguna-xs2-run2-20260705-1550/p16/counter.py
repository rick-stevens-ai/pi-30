import threading

class SafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def incr(self):
        with self._lock:
            self._count = self._count + 1

    def value(self):
        with self._lock:
            return self._count