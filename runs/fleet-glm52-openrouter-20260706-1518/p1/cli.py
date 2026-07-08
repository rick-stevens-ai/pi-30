import sys
import math


def main():
    data = sys.stdin.read()
    nums = [float(x) for x in data.split()]
    n = len(nums)
    if n == 0:
        print("count=0 min= max= mean= median= stdev=")
        return
    mn = min(nums)
    mx = max(nums)
    mean = sum(nums) / n
    s = sorted(nums)
    if n % 2 == 1:
        median = s[n // 2]
    else:
        median = (s[n // 2 - 1] + s[n // 2]) / 2.0
    if n == 1:
        stdev = 0.0
    else:
        var = sum((x - mean) ** 2 for x in nums) / (n - 1)
        stdev = math.sqrt(var)
    print(f"count={n} min={mn} max={mx} mean={mean} median={median} stdev={stdev}")


if __name__ == "__main__":
    main()
