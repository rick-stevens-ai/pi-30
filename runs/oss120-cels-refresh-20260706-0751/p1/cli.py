#!/usr/bin/env python3
"""CLI tool that reads whitespace/newline separated numbers from STDIN and prints statistics.

Output format (single line):
    count=N min=.. max=.. mean=.. median=.. stdev=..
where:
* count – integer number of values
* min, max, mean, median, stdev – floating‑point numbers (sample standard deviation, i.e. denominator n‑1)

The script uses only the Python standard library and exits with status 0.
"""

import sys
import statistics

def main() -> None:
    # Read all data from stdin, split on any whitespace, and convert to float.
    data_str = sys.stdin.read().strip()
    if not data_str:
        # No numbers – print zeros/empty stats as a graceful fallback.
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return

    numbers = [float(x) for x in data_str.split()]

    cnt = len(numbers)
    mn = min(numbers)
    mx = max(numbers)
    mean = statistics.mean(numbers)
    median = statistics.median(numbers)
    # Sample standard deviation uses n-1 denominator; if only one value, stdev is 0.
    stdev = statistics.stdev(numbers) if cnt > 1 else 0.0

    # Use the default string conversion for floats – matches the requirement of stdlib only.
    print(f"count={cnt} min={mn} max={mx} mean={mean} median={median} stdev={stdev}")

if __name__ == "__main__":
    main()
