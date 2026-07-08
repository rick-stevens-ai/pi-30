#!/usr/bin/env python3
"""
Read whitespace/newline-separated numbers from STDIN and output statistics.

The output is a single line in the form:
    count=N min=.. max=.. mean=.. median=.. stdev=..
where all values are represented using Python's default float formatting.
"""
import sys, math

def main() -> None:
    data = sys.stdin.read().strip()
    if not data:
        # No numbers – exit with count 0 and no further stats
        print("count=0")
        return
    try:
        nums = [float(x) for x in data.split()]
    except ValueError as e:
        sys.stderr.write(f"error: non-numeric input encountered\n")
        sys.exit(1)
    n = len(nums)
    total = sum(nums)
    mean = total / n
    mn = min(nums)
    mx = max(nums)
    sorted_nums = sorted(nums)
    if n % 2:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    # Sample standard deviation, denominator n-1
    if n > 1:
        var_sum = sum((x - mean) ** 2 for x in nums)
        stdev = math.sqrt(var_sum / (n - 1))
    else:
        stdev = 0.0
    print(f"count={n} min={mn} max={mx} mean={mean} median={median} stdev={stdev}")

if __name__ == "__main__":
    main()
