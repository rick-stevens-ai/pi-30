import sys

def main():
    data = list(map(float, sys.stdin.read().split()))
    n = len(data)
    if n == 0:
        print('count=0 min= max= mean= median= stdev=')
        return
    min_val = min(data)
    max_val = max(data)
    mean = sum(data) / n
    sorted_data = sorted(data)
    mid = n // 2
    if n % 2 == 1:
        median = sorted_data[mid]
    else:
        median = (sorted_data[mid-1] + sorted_data[mid]) / 2.0
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    std = variance ** 0.5
    print(f'count={n} min={min_val} max={max_val} mean={mean} median={median} stdev={std}')

if __name__ == '__main__':
    main()