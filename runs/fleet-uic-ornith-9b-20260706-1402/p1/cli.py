import sys
import math


def main():
    nums = []
    for line in sys.stdin:
        for token in line.split():
            try:
                nums.append(float(token))
            except ValueError:
                pass

    count = len(nums)
    if count == 0:
        print("count=0 min= max= mean= median= stdev=")
        sys.exit(0)

    sorted_nums = sorted(nums)
    minimum = min(sorted_nums)
    maximum = max(sorted_nums)

    # Mean
    total = sum(sorted_nums)
    mean = total / count

    # Median
    if count % 2 == 1:
        median = sorted_nums[count // 2]
    else:
        mid = count // 2
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

    # Sample standard deviation (n-1)
    variance_sum = sum((x - mean) ** 2 for x in sorted_nums)
    stdev = math.sqrt(variance_sum / (count - 1))

    print(f"count={count} min={minimum:.6f} max={maximum:.6f} mean={mean:.6f} median={median:.6f} stdev={stdev:.6f}")


if __name__ == "__main__":
    main()
