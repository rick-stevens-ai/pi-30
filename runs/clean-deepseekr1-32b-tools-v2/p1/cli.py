import math
import statistics
from sys import stdin

def main():
    try:
        numbers = list(map(float, stdin.read().split()))
    except ValueError as e:
        print(f'Error: Invalid input - {e}', file=sys.stderr)
        return 1
    
    if not numbers:
        print('Usage: echo "1 2 3" | python cli.py')
        return 1
    
    count = len(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    mean = sum(numbers) / count
    sorted_numbers = sorted(numbers)
    median = statistics.median(sorted_numbers)
    stdev = statistics.stdev(sorted_numbers)
    
    print(f'count={count} min={min_val:.4f} max={max_val:.4f} mean={mean:.4f} median={median:.4f} stdev={stdev:.4f}')
    return 0

if __name__ == '__main__':
    exit(main())