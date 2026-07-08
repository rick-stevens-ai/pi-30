import sys
import math

def main():
    try:
        # Read all whitespace-separated numbers from STDIN
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        nums = [float(x) for x in input_data]
    except (EOFError, ValueError):
        sys.exit(0)

    n = len(nums)
    if n == 0:
        return

    # Basic statistics
    c_min = min(nums)
    c_max = max(nums)
    c_mean = sum(nums) / n
    
    # Median calculation
    sorted_nums = sorted(nums)
    if n % 2 == 1:
        c_median = sorted_nums[n // 2]
    else:
        c_median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2

    # Sample standard deviation (n-1)
    if n > 1:
        variance = sum((x - c_mean)**2 for x in nums) / (n - 1)
        c_stdev = math.sqrt(variance)
    else:
        c_stdev = 0.0

    print(f"count={n} min={c_min} max={c_max} mean={c_mean} median={c_median} stdev={c_stdev}")

if __name__ == "__main__":
    main()
