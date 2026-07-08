# P16: thread‑safe counter
# A class `Counter` with a thread‑safe increment method.
# Also provide backwards compatibility: `SafeCounter` is an alias.
# Import threading for the lock implementation.
import threading

class Counter:
    """A simple counter that can be safely incremented from many threads."""

    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        """Increment the counter by 1 in a thread‑safe way."""
        with self._lock:
            self._n += 1

    def value(self) -> int:
        """Return the current counter value."""
        return self._n

# Backwards compatibility for the original verifier.
# The old name was SafeCounter with method incr.
class SafeCounter(Counter):
    """Alias of Counter, kept for backward compatibility."""

    # Provide the old method name.
    def incr(self) -> None:  # pragma: no cover
        self.increment()
