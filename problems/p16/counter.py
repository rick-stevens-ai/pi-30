# P16 SEED: unsynchronized counter with a DETERMINISTIC read-modify-write race.
# incr() reads the current value into a local, yields the GIL (time.sleep(0)),
# then writes value+1 back. Under concurrent threads this reliably loses updates
# because many threads read the same stale value before any writes back. A correct
# solution (threading.Lock around the whole read-modify-write, or an atomic
# pattern) makes the final count exact. Do NOT remove the yield to "fix" it —
# the fix is mutual exclusion, not hiding the race.
import time


class SafeCounter:
    def __init__(self):
        self._n = 0

    def incr(self):
        tmp = self._n          # read
        time.sleep(0)          # yield the GIL -> exposes the race deterministically
        self._n = tmp + 1      # write (not atomic: lost updates under contention)

    def value(self):
        return self._n
