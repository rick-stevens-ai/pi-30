# Merges overlapping intervals into a sorted list of non-overlapping intervals.
def merge(ivs):
    if not ivs:
        return []
    
    # 1. Sort intervals by start time
    sorted_ivs = sorted(list(ivs))
    
    merged = [list(sorted_ivs[0])]
    
    for next_start, next_end in sorted_ivs[1:]:
        current_merge = merged[-1]
        current_end = current_merge[1]

        # Check for overlap or adjacency (next_start <= current_end)
        if next_start <= current_end:
            # Merge: extend the end time if necessary
            current_merge[1] = max(current_end, next_end)
        else:
            # No overlap, start a new merged interval
            merged.append([next_start, next_end])
    
    # Convert internal lists back to tuples for consistent output format
    return [tuple(i) for i in merged]
