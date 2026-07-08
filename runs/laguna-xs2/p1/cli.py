#!/usr/bin/env python3
"""Read numbers from STDIN and compute statistics."""

import sys
import math


def main():
    # Read all input and split on whitespace
    data = sys.stdin.read().strip()
    if not data:
        print("count=0 min= max= mean= median= stdev=")
        sys.exit(0)
    
    numbers = [float(x) for x in data.split()]
    n = len(numbers)
    
    # Sort for median
    sorted_nums = sorted(numbers)
    
    # Compute statistics
    count = n
    min_val = sorted_nums[0]
    max_val = sorted_nums[-1]
    mean = sum(sorted_nums) / n
    
    # Median
    if n % 2 == 1:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
    
    # Sample standard deviation (n-1 denominator)
    if n > 1:
        variance = sum((x - mean) ** 2 for x in sorted_nums) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0
    
    print(f"count={count} min={min_val} max={max_val} mean={mean} median={median} stdev={stdev}")
    sys.exit(0)


if __name__ == "__main__":
    main()