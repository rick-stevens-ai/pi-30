#!/usr/bin/env python3
import sys
import math

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    numbers = [float(x) for x in data]
    n = len(numbers)
    
    numbers_sorted = sorted(numbers)
    min_val = numbers_sorted[0]
    max_val = numbers_sorted[-1]
    mean_val = sum(numbers) / n
    
    # median
    mid = n // 2
    if n % 2 == 1:
        median_val = numbers_sorted[mid]
    else:
        median_val = (numbers_sorted[mid - 1] + numbers_sorted[mid]) / 2
    
    # sample standard deviation (n-1)
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in numbers) / (n - 1)
        stdev_val = math.sqrt(variance)
    else:
        stdev_val = 0.0
    
    # format output
    # Use repr-like formatting but without unnecessary precision
    def fmt(x):
        # Print as int if it's a whole number, otherwise as float
        if abs(x - round(x)) < 1e-12:
            return str(int(round(x)))
        return f"{x:.10g}"
    
    print(f"count={n} min={fmt(min_val)} max={fmt(max_val)} mean={fmt(mean_val)} median={fmt(median_val)} stdev={fmt(stdev_val)}")

if __name__ == "__main__":
    main()