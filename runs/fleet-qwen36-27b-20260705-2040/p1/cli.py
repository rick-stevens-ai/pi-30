import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        print("count=0 min= min= mean= median= stdev=")
        sys.exit(0)

    nums = [float(x) for x in data]
    n = len(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = sum(nums) / n

    sorted_nums = sorted(nums)
    if n % 2 == 1:
        median_val = sorted_nums[n // 2]
    else:
        median_val = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0

    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in nums) / (n - 1)
        stdev_val = math.sqrt(variance)
    else:
        stdev_val = 0.0

    def fmt(v):
        if v == int(v):
            return str(int(v))
        return f"{v:g}"

    print(f"count={n} min={fmt(min_val)} max={fmt(max_val)} mean={fmt(mean_val)} median={fmt(median_val)} stdev={fmt(stdev_val)}")
    sys.exit(0)

if __name__ == "__main__":
    main()
