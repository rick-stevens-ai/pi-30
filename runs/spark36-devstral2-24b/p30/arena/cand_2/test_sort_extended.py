#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from sort import my_sort

# Test cases
test_cases = [
    ([], "empty list"),
    ([-5, -1, -3], "negative numbers only"),
    ([2, 1, 2, 3, 1], "duplicates only"),
    ([-2, 0, -1, 5, 3, -1], "mixed negatives and positives with duplicates"),
    ([3, 1, 4, 1, 5, 9, 2], "general case"),
    ([42], "single element"),
    ([1, 1, 1, 1], "all identical"),
]

for arr, desc in test_cases:
    result = my_sort(arr)
    original_multiset = sorted(arr)
    result_multiset = sorted(result)
    print(f"{desc:40s} -> {'PASS' if result_multiset == original_multiset else 'FAIL'}")
    if result_multiset != original_multiset:
        print(f"  Original multiset: {original_multiset}")
        print(f"  Result multiset:   {result_multiset}")
