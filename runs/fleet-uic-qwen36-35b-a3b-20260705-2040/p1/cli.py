import sys, math

nums = sorted(float(x) for line in sys.stdin for x in line.split())
n = len(nums)
if n == 0:
    sys.exit(0)

mean = sum(nums) / n
median = (nums[n // 2 - 1] + nums[n // 2]) / 2 if n % 2 == 0 else nums[n // 2]
stdev = math.sqrt(sum((x - mean) ** 2 for x in nums) / (n - 1)) if n > 1 else 0.0

print(f'count={n} min={nums[0]} max={nums[-1]} mean={mean:.5f} median={median:.5f} stdev={stdev:.5f}')
