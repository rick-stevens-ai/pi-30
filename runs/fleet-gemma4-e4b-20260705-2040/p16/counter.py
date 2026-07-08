import threading
class Counter:
    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._n += 1 # Atomic operation now

    def value(self):
        with self._lock:
            return self._n
