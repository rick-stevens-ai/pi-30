from stage import fmt

def test_fmt():
    # Test case 1: Normal dict
    d1 = {'b': 2, 'a': 1, 'c': 3}
    expected1 = "a=1 b=2 c=3"
    assert fmt(d1) == expected1

    # Test case 2: Single element
    d2 = {'z': 99}
    expected2 = "z=99"
    assert fmt(d2) == expected2

    # Test case 3: Empty dict
    d3 = {}
    expected3 = ""
    assert fmt(d3) == expected3

    # Test case 4: Mixed types of values (though PLAN says agg returns float/int/etc)
    d4 = {'count': 10, 'mean': 5.5}
    expected4 = "count=10 mean=5.5"
    assert fmt(d4) == expected4

    print("All tests passed!")

if __name__ == "__main__":
    test_fmt()
