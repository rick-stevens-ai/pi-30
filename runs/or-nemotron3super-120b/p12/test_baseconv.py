import baseconv
import random

def test():
    random.seed(42)
    for base in range(2, 37):
        for _ in range(1000):
            n = random.randint(-1000000, 1000000)
            s = baseconv.to_base(n, base)
            # ensure lowercase
            assert s == s.lower()
            # ensure no invalid characters
            for ch in s.lstrip('-'):
                if ch.isdigit():
                    val = ord(ch) - ord('0')
                else:
                    val = ord(ch) - ord('a') + 10
                assert 0 <= val < base
            # round-trip
            n2 = baseconv.parse_int(s, base)
            assert n == n2, f"Failed: n={n}, base={base}, s={s}, n2={n2}"
        # test zero
        assert baseconv.to_base(0, base) == '0'
        assert baseconv.parse_int('0', base) == 0
        # test negative zero? not needed
        # test max/min?
    print("All tests passed")

if __name__ == "__main__":
    test()
