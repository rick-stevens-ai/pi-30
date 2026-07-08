#!/usr/bin/env python3
"""
Read whitespace/newline‑separated numbers from STDIN and print statistics.

Output format:
    count=N min=.. max=.. mean=.. median=.. stdev=..

`stdev` is the sample standard deviation (denominator n‑1).
Exits with code 0.
"""

import sys
import math

def main() -> None:
    data = sys.stdin.read().strip()
    if not data:
        numbers: list[float] = []
    else:
        try:
            numbers = [float(tok) for tok in data.split()]
        except ValueError:
            sys.exit(1)  # non‑numeric input

    n = len(numbers)

    if n == 0:
        # No לינám or any meaningful metric; use NaN
        min_val = max_val = mean_val = median_val = stdev_val = float("nan")
    else:
        min_val = min(numbers)
        max_val = max(numbers)
        mean_val = sum(numbers) / n

        sorted_nums = sorted(numbers)
        if n % 2 == 1:
            median_val = sorted_nums[n // 2]
        else:
            median_val = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2

        if n > 1:
            variance = sum((x - mean_val) ** 2 for x in numbers) / (n - 1)
            stdev_val = math.sqrt(variance)
        else:
            stdev_val = float("nan")

    print(
        f"count={n} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}"
    )

if __name__ == "__main__":
    main()
