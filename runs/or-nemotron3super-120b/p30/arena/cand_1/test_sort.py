import sys
sys.path.insert(0, '.')
from sort import my_sort

def test_stability():
    # Test stability: elements with same value but different identity (e.g., tuples with index)
    # We'll use list of pairs (value, original_index)
    data = [(3, 0), (1, 1), (2, 2), (3, 3), (1, 4)]
    # Sort by value only, but we want to see if original order of equal values preserved.
    # We'll extract values and sort using my_sort on values, but we need to track stability.
    # Better: sort list of tuples by first element; stability means that for equal first elements,
    # the second element (original index) should be in increasing order.
    sorted_data = my_sort(data)
    print("Sorted data:", sorted_data)
    # Check that the sequence of second elements for each value is increasing.
    from itertools import groupby
    for value, group in groupby(sorted_data, key=lambda x: x[0]):
        indices = [idx for (_, idx) in group]
        if indices != sorted(indices):
            print(f"FAIL: indices for value {value} are not in original order: {indices}")
            return False
    print("PASS stability")
    return True

def test_edge_cases():
    # empty
    assert my_sort([]) == []
    # singleton
    assert my_sort([5]) == [5]
    # duplicates
    assert my_sort([2, 2, 1, 1, 3]) == [1, 1, 2, 2, 3]
    # negatives
    assert my_sort([-5, 0, 5, -2]) == [-5, -2, 0, 5]
    # large ints
    assert my_sort([10**100, 10**50, 10**150]) == [10**50, 10**100, 10**150]
    # already sorted
    assert my_sort([1,2,3,4]) == [1,2,3,4]
    # reverse sorted
    assert my_sort([4,3,2,1]) == [1,2,3,4]
    print("All edge cases passed")
    return True

if __name__ == "__main__":
    ok = test_edge_cases() and test_stability()
    if ok:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("TESTS FAILED")
        sys.exit(1)
