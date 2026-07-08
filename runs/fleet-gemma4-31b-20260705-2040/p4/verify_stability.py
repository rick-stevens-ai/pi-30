import math
from fast import softmax

def test_softmax():
    test_cases = [
        ([800.0, 801.0, 802.0], "overflow case"),
        ([-1000.0, -1000.0, -999.0], "underflow case"),
        ([0.0, 0.0, 0.0], "zeros"),
        ([1.0, 2.0, 3.0, 4.0], "normal"),
        ([1e3, -1e3, 0.0], "mixed large"),
    ]
    
    for xs, name in test_cases:
        try:
            res = softmax(xs)
            print(f"{name}: {xs} -> {res}")
            assert len(res) == len(xs)
            assert abs(sum(res) - 1.0) < 1e-9
            for val in res:
                assert not math.isnan(val) and not math.isinf(val)
        except Exception as e:
            print(f"{name}: {xs} -> ERROR: {e}")

if __name__ == "__main__":
    test_softmax()
