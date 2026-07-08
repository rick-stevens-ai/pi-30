import sys, statistics

nums = [float(x) for x in sys.stdin.read().split() if x]

sys.stdout.write(
    f"count={len(nums)} min={min(nums)} max={max(nums)} "
    f"mean={statistics.mean(nums)} median={statistics.median(nums)} stdev={statistics.stdev(nums)}\n"
)
