# Data race analysis of SafeCounter class

The current implementation has a critical data race vulnerability due to unsynchronized access to the shared `_n` counter.

Specifically:
1. The `incr()` method performs a read-modify-write operation without any locking mechanism
2. The `value()` method reads the counter value without ensuring atomicity in high-contention environments

To fix this, we need to add proper thread-safe synchronization using threading.Lock to ensure exclusive access during both increment and read operations.