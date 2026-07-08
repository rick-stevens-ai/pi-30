import sys
import math

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    try:
        numbers = [float(x) for x in input_data]
    except ValueError:
        return

    n = len(numbers)
    if n == 0:
        return

    min_val = min(numbers)
    max_val = max(numbers)
    mean = sum(numbers) / n

    sorted_nums = sorted(numbers)
    if n % 2 == 1:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0

    if n > 1:
        variance = sum((x - mean) ** 2 for x in numbers) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0

    print(f"count={n} min={min_val} max={max_val} mean={mean} median={median} stdev={stdev}")

if __name__ == "__main__":
    main()
