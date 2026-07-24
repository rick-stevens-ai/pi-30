#!/usr/bin/env python3
"""Stats tool: reads whitespace/newline-separated numbers from STDIN,
prints one line: count=N min=.. max=.. mean=.. median=.. stdev=..
(stdev is SAMPLE stdev, i.e. denominator n-1)."""
import sys
import math


def main():
    data = sys.stdin.read().split()
    nums = [float(x) for x in data]
    n = len(nums)

    if n == 0:
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return

    nums.sort()

    mn = nums[0]
    mx = nums[-1]
    mean = sum(nums) / n

    # median: avg of two middle values when count is even
    if n % 2 == 1:
        median = nums[n // 2]
    else:
        median = (nums[n // 2 - 1] + nums[n // 2]) / 2.0

    # sample stdev (n-1 denominator)
    if n > 1:
        variance = sum((x - mean) ** 2 for x in nums) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0

    print(f"count={n} min={mn} max={mx} mean={mean} median={median} stdev={stdev}")


if __name__ == "__main__":
    main()