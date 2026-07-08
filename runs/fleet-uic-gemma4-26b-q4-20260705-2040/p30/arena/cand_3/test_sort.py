from sort import my_sort

def test_stability():
    # Stability test: using tuples where the first element is the sort key
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
    # We want to sort by the first element of the tuple
    # But my_sort uses the default comparison for tuples, which is lexicographical.
    # So it already does what we want if we're comparing tuples.
    # Wait, if I pass [(2, 'a'), (1, 'b'), (2, 'c')], sorted() compares (2, 'a') vs (1, 'b').
    # It will put (1, 'b') first, then (2, 'a'), then (2, 'c').
    # Actually, for tuples, it's stable if the first elements are equal.
    
    # Let's use a class that only compares on one attribute to truly test stability.
    class StableElement:
        def __init__(self, val, original_index):
            self.val = val
            self.original_index = original_index
        
        def __lt__(self, other):
            return self.val < other.val
        
        def __eq__(self, other):
            return self.val == other.val

        def __repr__(self):
            return f"({self.val}, {self.original_index})"

    elements = [StableElement(2, 0), StableElement(1, 1), StableElement(2, 2), StableElement(1, 3), StableElement(3, 4)]
    # Expected sorted order based on val:
    # (1, 1), (1, 3), (2, 0), (2, 2), (3, 4)
    sorted_elements = my_sort(elements)
    expected = [(1, 1), (1, 3), (2, 0), (2, 2), (3, 4)]
    actual = [(e.val, e.original_index) for e in sorted_elements]
    
    print(f"Actual:   {actual}")
    print(f"Expected: {expected}")
    assert actual == expected, "Stability test failed!"

def test_multiset():
    # Test duplicates (multiset property)
    xs = [1, 2, 2, 3, 3, 3, 1]
    expected = [1, 1, 2, 2, 3, 3, 3]
    assert my_sort(xs) == expected

def test_empty():
    assert my_sort([]) == []

def test_negatives():
    assert my_sort([0, -1, -5, 10, -2]) == [-5, -2, -1, 0, 10]

if __name__ == "__main__":
    test_stability()
    test_multiset()
    test_empty()
    test_negatives()
    print("All advanced tests passed!")
