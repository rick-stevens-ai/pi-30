# Counter.py Data Race Critique

- The `incr` method of `SafeCounter` performs a read‑modify‑write (`self._n = self._n + 1`) without any synchronization.
- This creates a data race because multiple threads can execute the statement concurrently, causing lost updates and resulting in counts lower than expected under high contention (the GIL does not protect bytecode interleaving).
- Missing lock on the shared variable `_n`.
- Recommended fix: introduce a `threading.Lock` protecting the increment or switch to an atomic primitive/itertools pattern.