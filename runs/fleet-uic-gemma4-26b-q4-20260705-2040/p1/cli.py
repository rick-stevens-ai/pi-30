import sys
import math

def main():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return

        nums = [float(x) for x in input_data]
        n = len(nums)
        
        if n == 0:
            return

        count = n
        minimum = min(nums)
        maximum = max(nums)
        mean = sum(nums) / n

        # Median
        sorted_nums = sorted(nums)
        if n % 2 == 1:
            median = sorted_nums[n // 2]
        else:
            median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2

        # Sample Stdev (n-1)
        if n > 1:
            variance_sum = sum((x - mean) ** 2 for x in nums)
            stdev = math.sqrt(variance_sum / (n - 1))
        else:
            stdev = 0.0 # Or some representation of undefined, but 0.0 is common if n=1 and we want to avoid errors

        # Formatting: The prompt says 'min=.. max=..' etc. 
        # It doesn't specify precision. I will use a default string representation or format it nicely.
        # Usually, when asked for "exactly one line" with that pattern, it implies some formatting.
        print(f"count={count} min={minimum} max={maximum} mean={mean} median={median} stdev={stdev}")

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
