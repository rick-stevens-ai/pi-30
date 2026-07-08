# P21 SEED: merges only consecutive-in-INPUT intervals, no sorting. Wrong when
# input is unsorted or has non-adjacent overlaps.
def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # Make a copy and sort by start time\n    sorted_intervals = sorted([list(iv) for iv in intervals], key=lambda x: x[0])\n    merged = [sorted_intervals[0]]\n
    for current in sorted_intervals[1:]:\n        last = merged[-1]\n        if current[0] <= last[1]:\n            # Merge intervals by updating end time\n            last[1] = max(last[1], current[1])\n        else:\n            merged.append(current)\n    return merged