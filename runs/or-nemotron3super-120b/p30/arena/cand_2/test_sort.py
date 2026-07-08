import sys
sys.path.insert(0, '.')

from sort import my_sort

def test_stability():
    # Test stability: elements with same key but different id
    # We'll use tuples (value, index) and sort by value only.
    data = [(3, 'a'), (2, 'b'), (3, 'c'), (1, 'd'), (2, 'e')]
    # Extract values for sorting
    xs = [v for v, _ in data]
    sorted_xs = my_sort(xs)
    print("Input:", xs)
    print("Sorted:", sorted_xs)
    # Expected sorted values: [1,2,2,3,3]
    expected = [1,2,2,3,3]
    assert sorted_xs == expected, f"Expected {expected}, got {sorted_xs}"
    # To check stability, we need to see if the relative order of equal values is preserved.
    # Since we sorted only values, we can't directly see stability from values alone.
    # Instead we can sort list of tuples by first element using a stable sort and compare.
    # But we can simulate by tagging each element with its original position.
    indexed = [(v, i) for i, v in enumerate(xs)]
    # Sort by value using my_sort on the first element? We need to sort tuples by first element.
    # Let's create a list of tuples and sort using my_sort with a custom key? Not possible.
    # Instead we can extract the sorted order of indices by using argsort via my_sort on values?
    # We'll do a simpler stability test: sort list of 0s and 1s with tags.
    # Create list of pairs (value, tag) where value is 0 or 1, tag is unique.
    # We'll sort by value using my_sort on the list of values, but we need to track tags.
    # We'll instead implement a decorator: we can sort list of tuples by first element using my_sort if we
    # modify my_sort to accept key? Not.
    # Let's just test with integers where duplicates are indistinguishable; stability not observable.
    # So we need to test with objects that compare equal but are distinct.
    # We'll define a class that compares equal based on value but has id.
    class Elem:
        def __init__(self, val, tag):
            self.val = val
            self.tag = tag
        def __lt__(self, other):
            return self.val < other.val
        def __le__(self, other):
            return self.val <= other.val
        def __eq__(self, other):
            return self.val == other.val
        def __repr__(self):
            return f"Elem({self.val},{self.tag})"
    elems = [Elem(3, 'a'), Elem(2, 'b'), Elem(3, 'c'), Elem(1, 'd'), Elem(2, 'e')]
    # We need to sort elems using my_sort. But my_sort works on list of items and uses <= operator.
    # Since we defined __le__, it should work.
    sorted_elems = my_sort(elems)
    print("Elem input:", elems)
    print("Elem sorted:", sorted_elems)
    # Extract values in order
    vals = [e.val for e in sorted_elems]
    tags = [e.tag for e in sorted_elems]
    print("Values:", vals)
    print("Tags:", tags)
    # Check that values are sorted
    assert vals == [1,2,2,3,3]
    # Check stability: For value 2, original order was 'b' then 'e' (indices 1 and 4)
    # In sorted list, the two 2s should appear in order 'b','e'
    # Find positions of value 2
    twos = [e.tag for e in sorted_elems if e.val == 2]
    print("Tags of 2s:", twos)
    assert twos == ['b', 'e'], f"Expected ['b','e'] for 2s, got {twos}"
    # For value 3, original order 'a' then 'c'
    threes = [e.tag for e in sorted_elems if e.val == 3]
    print("Tags of 3s:", threes)
    assert threes == ['a', 'c'], f"Expected ['a','c'] for 3s, got {threes}"
    print("Stability test passed")

def test_edge_cases():
    # Empty
    assert my_sort([]) == []
    # Singleton
    assert my_sort([5]) == [5]
    # Duplicates
    assert my_sort([2,2,2]) == [2,2,2]
    # Negatives
    assert my_sort([3,-1,0,-5,2]) == [-5,-1,0,2,3]
    # Already sorted
    assert my_sort([1,2,3]) == [1,2,3]
    # Reverse sorted
    assert my_sort([3,2,1]) == [1,2,3]
    # Large integers
    big = 10**100
    assert my_sort([big, -big, 0]) == [-big, 0, big]
    print("Edge cases passed")

if __name__ == "__main__":
    test_stability()
    test_edge_cases()
    print("All tests passed")