import sys
import math

def calculate_median(data):
    """Calculates the median of a list of numbers."""
    if not data:
        return None
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        # Odd number of elements
        return sorted_data[n // 2]
    else:
        # Even number of elements, average of the two middle ones
        mid1 = sorted_data[n // 2 - 1]
        mid2 = sorted_data[n // 2]
        return (mid1 + mid2) / 2

def calculate_sample_stdev(data, mean):
    """Calculates the sample standard deviation (using n-1)."""
    n = len(data)
    if n < 2:
        # Sample standard deviation is undefined or often treated as NaN/0 for N<2.
        # We'll return 0.0 if we must provide a number, though the calculation logic below handles division by zero.
        return 0.0

    variance_sum = sum([(x - mean) ** 2 for x in data])
    # Sample standard deviation: sqrt(sum((x_i - mean)^2) / (n - 1))
    return math.sqrt(variance_sum / (n - 1))


def main():
    # Read all input from STDIN, split by any whitespace (including newlines)
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            # Handle case where no input is provided
            print("count=0 min=.. max=.. mean=.. median=.. stdev=..")
            sys.exit(0)

        # Parse numbers. We split by whitespace and try to convert each part to float.
        numbers = []
        for item in input_data.split():
            try:
                numbers.append(float(item))
            except ValueError:
                # Ignore items that cannot be converted to float
                continue

    except Exception as e:
        # Handle potential reading errors, though unlikely for sys.stdin.read()
        sys.stderr.write(f"Error reading input: {e}\n")
        sys.exit(1)

    N = len(numbers)

    if N == 0:
        print("count=0 min=.. max=.. mean=.. median=.. stdev=..")
        sys.exit(0)

    # 1. Basic stats
    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = sum(numbers) / N
    median_val = calculate_median(numbers)

    # 2. Standard deviation
    stdev_val = 0.0
    if N >= 2:
        stdev_val = calculate_sample_stdev(numbers, mean_val)
    # If N=1, stdev remains 0.0 as per our implementation choice for N<2 cases.

    # Format output
    output = (f"count={N} min={min_val:.6f} max={max_val:.6f} "
              f"mean={mean_val:.6f} median={median_val:.6f} stdev={stdev_val:.6f}")

    print(output)

if __name__ == "__main__":
    main()