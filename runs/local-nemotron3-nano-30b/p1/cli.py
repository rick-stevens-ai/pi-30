#!/usr/bin/env python3
import sys

def main():
    data = sys.stdin.read().strip()
    tokens = data.split()
    numbers = list(map(float, tokens)) if tokens else []
    n = len(numbers)
    
    if n == 0:
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return

    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = sum(numbers) / n
    
    sorted_nums = sorted(numbers)
    mid = n // 2
    if n % 2 == 1:
        median_val = sorted_nums[mid]
    else:
        median_val = (sorted_nums[mid-1] + sorted_nums[mid]) / 2.0
    
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in numbers) / (n - 1)
        stdev_val = variance ** 0.5
    else:
        stdev_val = 0.0

    print(f"count={n} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}")

if __name__ == "__main__":
    main()