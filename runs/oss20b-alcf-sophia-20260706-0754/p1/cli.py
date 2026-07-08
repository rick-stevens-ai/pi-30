#!/usr/bin/env python3
"""
Read whitespace/newline-separated numbers from STDIN and print statistics.

The output is a single line in the format:
  count=N min=.. max=.. mean=.. median=.. stdev=..

All calculations use the stdlib module `statistics`.

Sample stddev (i.e., n-1 in the denominator) is used.

The script exits with status 0.
"""

import sys
import statistics


def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        # No numbers provided – output zeros for all metrics.
        count = 0
        min_val = max_val = mean_val = median_val = stdev_val = 0.0
    else:
        numbers = [float(x) for x in data]
        count = len(numbers)
        min_val = min(numbers)
        max_val = max(numbers)
        mean_val = statistics.mean(numbers)
        median_val = statistics.median(numbers)
        # For a single value statistics.stdev raises StatisticsError.
        if count > 1:
            stdev_val = statistics.stdev(numbers)
        else:
            stdev_val = 0.0

    output = f"count={count} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}"
    print(output)


if __name__ == "__main__":
    main()
