import sys
import statistics
import math

def calculate_statistics(numbers):
    """Calculates count, min, max, mean, median, and sample standard deviation."""
    count = len(numbers)
    if count == 0:
        return None # Handle empty input case gracefully if needed, though the prompt implies numbers will be present.

    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = sum(numbers) / count
    
    # Median calculation
    sorted_numbers = sorted(numbers)
    if count % 2 == 1:
        median_val = sorted_numbers[count // 2]
    else:
        mid1 = sorted_numbers[count // 2 - 1]
        mid2 = sorted_numbers[count // 2]
        median_val = (mid1 + mid2) / 2.0

    # Sample Standard Deviation (N-1 denominator)
    if count > 1:
        variance = sum((x - mean_val) ** 2 for x in numbers) / (count - 1)
        stdev_val = math.sqrt(variance)
    else:
        stdev_val = 0.0 # Stdev is undefined or zero if count <= 1

    return {
        "count": count,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "median": median_val,
        "stdev": stdev_val
    }

def main():
    # Read all numbers from STDIN, handling whitespace/newline separation.
    try:
        data = sys.stdin.read().split()
        if not data:
            # Handle case where no input is provided
            print("count=0 min=N/A max=N/A mean=N/A median=N/A stdev=0.0")
            sys.exit(0)
            
        numbers = [float(x) for x in data]
    except ValueError:
        # Handle non-numeric input if necessary, though the prompt assumes valid numbers.
        print("Error: Input must be whitespace/newline-separated numbers.")
        sys.exit(1)

    stats = calculate_statistics(numbers)

    if stats:
        output = (f"count={stats['count']} "
                  f"min={stats['min']:.2f} "
                  f"max={stats['max']:.2f} "
                  f"mean={stats['mean']:.2f} "
                  f"median={stats['median']:.2f} "
                  f"stdev={stats['stdev']:.2f}")
        print(output)

    sys.exit(0)

if __name__ == "__main__":
    # Note: Using standard library functions only (math, sys). 
    # We implemented median and stdev manually to ensure adherence if the 'statistics' module was disallowed, 
    # but since we are using stdlib, it is fine. I will stick to manual implementation for robustness against stricter interpretations.
    main()