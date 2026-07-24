#!/usr/bin/env python3
import sys, math

def main():
    nums = []
    for line in sys.stdin:
        for token in line.split():
            if token:
                nums.append(float(token))
    n = len(nums)
    if n == 0:
        print("count=0 min=.. max=.. mean=.. median=.. stdev=..")
        return
    nums.sort()
    min_val = nums[0]
    max_val = nums[-1]
    mean_val = sum(nums) / n
    if n % 2 == 1:
        median_val = nums[n // 2]
    else:
        median_val = (nums[n // 2 - 1] + nums[n // 2]) / 2.0
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in nums) / (n - 1)
        stdev_val = math.sqrt(variance)
    else:
        stdev_val = 0.0
    print(f"count={n} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}")

if __name__ == "__main__":
    main()
    sys.exit(0)
