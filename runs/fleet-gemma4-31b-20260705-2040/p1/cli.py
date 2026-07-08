import sys
import math

def main():
    # Read all whitespace/newline separated numbers from STDIN
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return # Or print nothing and exit 0 as per "Exit 0" requirement.
        
        numbers = [float(x) for x in input_data]
    except EOFError:
        return
    except ValueError:
        # Handle cases where non-numeric data is provided if necessary, 
        # though typically not expected based on prompt.
        return

    n = len(numbers)
    if n == 0:
        return

    s_min = min(numbers)
    s_max = max(numbers)
    s_mean = sum(numbers) / n
    
    # Median calculation
    sorted_nums = sorted(numbers)
    if n % 2 == 1:
        s_median = sorted_nums[n // 2]
    else:
        s_median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0

    # Sample Standard Deviation calculation (n-1)
    if n > 1:
        variance = sum((x - s_mean) ** 2 for x in numbers) / (n - 1)
        s_stdev = math.sqrt(variance)
    else:
        s_stdev = 0.0 # Sample stdev is undefined for n=1, but we use 0.0 to maintain the line format

    print(f"count={n} min={s_min} max={s_max} mean={s_mean} median={s_median} stdev={s_stdev}")

if __name__ == "__main__":
    main()
