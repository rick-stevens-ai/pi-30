import sys
import statistics


def main():
    numbers = [float(x) for x in sys.stdin.read().split()]

    n = len(numbers)
    if n == 0:
        return

    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = sum(numbers) / n
    median_val = statistics.median(numbers)
    stdev_val = statistics.stdev(numbers)

    print(f"count={n} min={min_val:.6f} max={max_val:.6f} mean={mean_val:.6f} median={median_val:.6f} stdev={stdev_val:.6f}")


if __name__ == "__main__":
    main()
