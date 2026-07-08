import sys
import math


def main():
    numbers = []
    for line in sys.stdin:
        for token in line.split():
            try:
                numbers.append(float(token))
            except ValueError:
                continue

    if not numbers:
        print("count=0 min= max= mean= median= stdev=")
        return

    n = len(numbers)
    sorted_n = sorted(numbers)
    mn = min(sorted_n)
    mx = max(sorted_n)
    mean = sum(sorted_n) / n

    if n % 2 == 1:
        median = sorted_n[n // 2]
    else:
        median = (sorted_n[n // 2 - 1] + sorted_n[n // 2]) / 2.0

    variance = sum((x - mean) ** 2 for x in sorted_n) / (n - 1)
    stdev = math.sqrt(variance)

    print(f"count={n} min={mn} max={mx} mean={mean} median={median} stdev={stdev}")


if __name__ == "__main__":
    main()
