#!/usr/bin/env python3
"""Read numbers from STDIN, print statistics."""

import sys
import math


def main() -> None:
    data = sys.stdin.read().split()
    numbers = [float(x) for x in data if x]

    if not numbers:
        print("count=0 min= max= mean= median= stdev=")
        sys.exit(0)

    n = len(numbers)
    sorted_nums = sorted(numbers)

    count = n
    min_val = sorted_nums[0]
    max_val = sorted_nums[-1]
    mean_val = sum(numbers) / n

    # Median
    mid = n // 2
    if n % 2 == 0:
        median_val = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median_val = sorted_nums[mid]

    # Sample standard deviation (n-1)
    if n == 1:
        stdev_val = 0.0
    else:
        variance = sum((x - mean_val) ** 2 for x in numbers) / (n - 1)
        stdev_val = math.sqrt(variance)

    print(f"count={count} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}")
    sys.exit(0)


if __name__ == "__main__":
    main()