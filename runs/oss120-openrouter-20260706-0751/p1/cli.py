#!/usr/bin/env python3
import sys
import math

def main() -> None:
    # Read all whitespace-separated tokens from stdin
    data = sys.stdin.read().strip().split()
    if not data:
        # No numbers, print count=0 and placeholders as NaN
        print('count=0 min=NaN max=NaN mean=NaN median=NaN stdev=NaN')
        return
    # Convert to floats
    try:
        nums = [float(x) for x in data]
    except ValueError:
        sys.exit('Invalid numeric input')
    n = len(nums)
    mn = min(nums)
    mx = max(nums)
    mean = sum(nums) / n
    # Median
    nums_sorted = sorted(nums)
    mid = n // 2
    if n % 2 == 1:
        median = nums_sorted[mid]
    else:
        median = (nums_sorted[mid - 1] + nums_sorted[mid]) / 2.0
    # Sample standard deviation (n-1 denominator)
    if n > 1:
        var = sum((x - mean) ** 2 for x in nums) / (n - 1)
        stdev = math.sqrt(var)
    else:
        stdev = float('nan')
    # Format output, using repr to avoid scientific notation issues? Use plain formatting
    print(f'count={n} min={mn} max={mx} mean={mean} median={median} stdev={stdev}')

if __name__ == '__main__':
    main()
