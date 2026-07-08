#!/usr/bin/env python3
import sys
import math

def main():
    # Read all input from stdin
    data = sys.stdin.read()
    
    # Split by whitespace and filter out empty strings
    numbers = data.replace('\n', ' ').split()
    
    # Convert to floats
    try:
        values = [float(x) for x in numbers]
    except ValueError:
        print("Error: Invalid input - not all tokens are numbers", file=sys.stderr)
        sys.exit(1)
    
    # Calculate statistics
    count = len(values)
    
    if count == 0:
        print("Error: No numbers provided", file=sys.stderr)
        sys.exit(1)
    
    min_val = min(values)
    max_val = max(values)
    mean = sum(values) / count
    
    # Calculate median
    sorted_values = sorted(values)
    mid = count // 2
    if count % 2 == 1:
        median = sorted_values[mid]
    else:
        median = (sorted_values[mid - 1] + sorted_values[mid]) / 2
    
    # Calculate sample standard deviation (n-1)
    if count == 1:
        stdev = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in values) / (count - 1)
        stdev = math.sqrt(variance)
    
    # Print results in one line
    print(f"count={count} min={min_val} max={max_val} mean={mean} median={median} stdev={stdev}")
    sys.exit(0)

if __name__ == "__main__":
    main()