import sys
import statistics

def main():
    data = []
    for line in sys.stdin:
        parts = line.strip().split()
        for p in parts:
            data.append(float(p))
    if not data:
        print("count=0 min=0 max=0 mean=0 median=0 stdev=0")
        return
    count = len(data)
    min_val = min(data)
    max_val = max(data)
    mean_val = statistics.mean(data)
    median_val = statistics.median(data)
    stdev_val = statistics.stdev(data)
    print(f"count={count} min={min_val} max={max_val} mean={mean_val} median={median_val} stdev={stdev_val}")

if __name__ == "__main__":
    main()