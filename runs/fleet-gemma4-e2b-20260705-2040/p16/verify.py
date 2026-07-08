# P16 generator+critic: a thread-safe bounded counter that must give the EXACT
# final count under heavy concurrent increment from many threads. Seed has a
# read-modify-write race (no lock) -> lost updates. Critic must catch the race.
#
# HARDENED: force the race deterministically by setting a very small thread
# switch interval so the interpreter preempts inside the read-modify-write
# window of the unsynchronized `self._n = self._n + 1`. A correct solution
# (threading.Lock) is immune; the naive seed loses updates.
import sys
sys.setswitchinterval(1e-6)  # force frequent preemption to expose the RMW race
from counter import SafeCounter
import threading


def main():
    c = SafeCounter()
    N_THREADS = 32
    PER = 40000
    def worker():
        for _ in range(PER):
            c.incr()
    threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
    for t in threads: t.start()
    for t in threads: t.join()
    expected = N_THREADS * PER
    got = c.value()
    if got != expected:
        print(f"RACE: got {got} expected {expected} (lost {expected-got} updates)")
        raise SystemExit(1)
    print(f"OK exact count {got}")


if __name__ == "__main__":
    main()
