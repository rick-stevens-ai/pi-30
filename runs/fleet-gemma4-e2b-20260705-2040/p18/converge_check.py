# P18 reflection: numerically-stable online variance (Welford). converge_check
# feeds a stream where the naive sum-of-squares formula catastrophically cancels
# (large mean, tiny variance) and goes negative/wrong. Loop must switch to
# Welford's algorithm and append a lesson to ~/.pi/agent/memory.md.
from stats import running_variance
import statistics

def main():
    # large offset + tiny spread -> sum-of-squares cancellation
    data = [1e9 + d for d in [0.0, 1.0, 2.0, 3.0, 4.0] * 2000]
    got = running_variance(data)              # sample variance (n-1)
    exp = statistics.variance(data)
    rel = abs(got - exp) / exp
    print(f"got={got:.6f} exp={exp:.6f} rel_err={rel:.3e}")
    if got < 0:
        print("NEGATIVE VARIANCE (catastrophic cancellation)")
        raise SystemExit(1)
    if rel > 1e-6:
        print("INACCURATE")
        raise SystemExit(1)
    # second stream: constant -> variance 0 exactly, no nan
    g2 = running_variance([2.5] * 1000)
    if abs(g2) > 1e-12:
        print(f"constant stream variance should be ~0, got {g2}")
        raise SystemExit(1)
    print("OK P18")

if __name__ == "__main__":
    main()
