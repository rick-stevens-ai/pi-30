#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from sort import my_sort

# Test empty list
print("Empty:", my_sort([]))

# Test with negatives
print("Negatives:", my_sort([-5, -1, -3]))

# Test with duplicates
print("Duplicates:", my_sort([2, 1, 2, 3, 1]))

# Test mixed
print("Mixed:", my_sort([-2, 0, -1, 5, 3, -1]))

# Multi-set preservation check
original = [3, 1, 4, 1, 5, 9, 2]
sorted_result = my_sort(original)
print("Original multiset:", sorted(sorted(original)))
print("Sorted multiset:  ", sorted(sorted_result))
print("Equal multisets:", sortedResult == sorted(original) if 'sortedResult' not in locals else False)
