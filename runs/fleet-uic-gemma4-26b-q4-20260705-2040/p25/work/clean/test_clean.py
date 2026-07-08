from stage import clean

def test():
    test_cases = [
        ([1, "2.5", None, "", "x", 3], [1.0, 2.5, 3.0]),
        (["1.1", "abc", "2.2"], [1.1, 2.2]),
        ([], []),
        ([None, None], []),
    ]
    for input_rows, expected in test_cases:
        actual = clean(input_rows)
        assert actual == expected, f"Failed: {input_rows} -> {actual}, expected {expected}"
    print("All tests passed!")

if __name__ == "__main__":
    test()
