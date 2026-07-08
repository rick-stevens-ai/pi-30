#!/usr/bin/env python3
"""CLI tool that reads whitespace/newline‑separated numbers from STDIN and prints statistics.

Output format (exactly one line)::

    count=N min=.. max=.. mean=.. median=.. stdev=..

* ``stdev`` is the *sample* standard deviation (denominator ``n-1``).
* For an even number of values the median is the average of the two central values.
* Uses only the Python standard library.
"""

import sys
import math

def main() -> None:
    # Read all input, split on any whitespace, ignore empty strings
    data = sys.stdin.read().strip().split()
    if not data:
        # No numbers – print zeros/defaults to keep a single line output
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return

    # Convert to float for calculations (int works as well)
    nums = [float(x) for x in data]
    n = len(nums)

    # Basic stats
    minimum = min(nums)
    maximum = max(nums)
    mean = sum(nums) / n

    # Median
    sorted_nums = sorted(nums)
    mid = n // 2
    if n % 2 == 1:
        median = sorted_nums[mid]
    else:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

    # Sample standard deviation (n-1 denominator). For n == 1, define stdev as 0.
    if n > 1:
        variance = sum((x - mean) ** 2 for x in nums) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0

    # Build the output line. Use ``repr`` to avoid locale‑dependent formatting.
    out = (
        f"count={n} "
        f"min={repr(minimum)} "
        f"max={repr(maximum)} "
        f"mean={repr(mean)} "
        f"median={repr(median)} "
        f"stdev={repr(stdev)}"
    )
    print(out)


if __name__ == "__main__":
    main()
