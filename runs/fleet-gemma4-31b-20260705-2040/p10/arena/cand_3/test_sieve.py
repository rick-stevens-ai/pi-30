import sieve

def test_primes():
    test_cases = [
        (0, []),
        (1, []),
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (5, [2, 3, 5]),
        (6, [2, 3, 5]),
        (7, [2, 3, 5, 7]),
        (8, [2, 3, 5, 7]),
        (9, [2, 3, 5, 7]),
        (10, [2, 3, 5, 7]),
        (11, [2, 3, 5, 7, 11]),
        (12, [2, 3, 5, 7, 11]),
        (13, [2, 3, 5, 7, 11, 13]),
        (25, [2, 3, 5, 7, 11, 13, 17, 19, 23]),
    ]
    for n, expected in test_cases:
        actual = sieve.primes_up_to(n)
        assert actual == expected, f"Failed for n={n}: expected {expected}, got {actual}"
    print("All tests passed!")

if __name__ == "__main__":
    test_primes()
