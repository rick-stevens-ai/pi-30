import sys
import math

def main():
    data = sys.stdin.read().strip()
    if not data:
        # No numbers: define zeros? but spec expects at least one number.
        # We'll output zeros to avoid crash.
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return
    parts = data.split()
    nums = []
    for p in parts:
        if p:
            try:
                nums.append(float(p))
            except ValueError:
                # ignore non-numeric?
                pass
    if not nums:
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return

    n = len(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean = sum(nums) / n
    sorted_nums = sorted(nums)
    if n % 2 == 1:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2.0
    if n >= 2:
        variance = sum((x - mean) ** 2 for x in nums) / (n - 1)
        stdev = math.sqrt(variance)
    else:
        stdev = 0.0

    # Format output
    out = f"count={n} min={min_val} max={max_val} mean={mean} median={median} stdev={stdev}"
    print(out)

if __name__ == "__main__":
    main()