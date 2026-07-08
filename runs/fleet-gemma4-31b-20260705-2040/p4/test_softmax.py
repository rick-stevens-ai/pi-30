from fast import softmax
import math

def test():
    xs = [800.0, 801.0, 802.0]
    print(f"Input: {xs}")
    print(f"Output: {softmax(xs)}")
    
    xs = [-1000.0, -1000.0, -999.0]
    print(f"Input: {xs}")
    print(f"Output: {softmax(xs)}")

if __name__ == "__main__":
    test()
