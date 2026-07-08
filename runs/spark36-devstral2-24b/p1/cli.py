#!/usr/bin/env python3
import sys

def calc_stats(numbers):
    """Calculate statistics for a list of numbers."""
    if not numbers:
        return {"count": 0}
    
    count = len(numbers)
    sorted_nums = sorted(numbers)
    
    minimum = min(sorted_nums)
    maximum = max(sorted_nums)
    mean = sum(sorted_nums) / count
    
    if count % 2 == 1:
        median = sorted_nums[count // 2]
    else:
        median = (sorted_nums[(count // 2) - 1] + sorted_nums[count // 2]) / 2
    
    variance_sum = 0.0
    for num in sorted_nums:
        variance_sum += (num - mean) ** 2
    stdev = (variance_sum / (count - 1)) ** 0.5 if count > 1 else 0.0
    
    return {
        "count": count,
        "min": minimum,
        "max": maximum,
        "mean": mean,
        "median": median,
        "stdev": stdev,
    }

def main():
    """Read numbers from STDIN and print statistics."""
    try:
        # Read all input at once
        input_text = sys.stdin.read()
        if not input_text.strip():
            stats = calc_stats([])
        else:
            numbers = []
            for item in input_text.replace(",", " ").split()]:
                num = float(item)
                numbers.append(num)
            stats = calc_stats(numbers)
    except Exception:
        sys.exit(1)
    
    # Format output
    print(
        f"count={stats['count']} "
        f"min={stats['min']} max={stats['max']} "
        f"mean={stats['mean']} median={stats['median']} stdev={stats['stdev']}"
    )

if __name__ == "__main__":
    main()