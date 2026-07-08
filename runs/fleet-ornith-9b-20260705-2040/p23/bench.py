# P23 benchmark — count_primes below N=1,000,000, prints a throughput metric.
import sys, time
from primecount import count_primes

def main():
    report = "--report" in sys.argv
    N = 1_000_000
    count_primes(1000)  # warm
    t0 = time.perf_counter(); count_primes(N); dt = time.perf_counter() - t0
    metric = N / dt / 1e6  # millions of n scanned per second
    print(f"{metric:.4f}" if report else f"count_primes({N}): {dt*1e3:.1f} ms  {metric:.3f} Mn/s")

if __name__ == "__main__":
    main()
