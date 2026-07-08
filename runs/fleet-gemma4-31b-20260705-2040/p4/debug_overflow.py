import math
from fast import softmax as fast_softmax

def test():
    xs = [800.0, 801.0, 802.0]
    try:
        print(f"Input: {xs}")
        print(f"Result: {fast_softmax(xs)}")
    except OverflowError as e:
        print(f"OverflowError: {e}")

if __name__ == "__main__":
    test()
