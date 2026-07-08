#!/usr/bin/env python3
import sys
import math

def main():
    data = []
    for line in sys.stdin:
        for token in line.split():
            data.append(float(token))
    
    n = len(data)
    if n == 0:
        print("count=0")
        sys.exit(0)
    
    data.sort()
    
    count = n
    min_val = data[0]
    max_val = data[-1]
    mean = sum(data) / n
    
    if n % 2 == 1:
        median = data[n // 2]
    else:
        median = (data[n // 2 - 1] + data[n // 2]) / 2
    
    if n > 1:
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0
    
    print(f"count={count} min={min_val} max={max_val} mean={mean} median={median} stdev={stdev}")
    sys.exit(0)

if __name__ == "__main__":
    main()