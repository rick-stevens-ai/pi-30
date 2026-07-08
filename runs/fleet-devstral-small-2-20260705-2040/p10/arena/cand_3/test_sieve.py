#!/usr/bin/env python3
"""Test cases to verify sieve.py correctness"""

def test_edge_cases():
    from sieve import primes_up_to
    
    # Test n < 2
    assert primes_up_to(0) == []
    assert primes_up_to(1) == []
    
    # Test n == 2
    assert primes_up_to(2) == [2]
    
    # Test small ranges
    assert primes_up_to(3) == [2, 3]
    assert primes_up_to(4) == [2, 3]
    assert primes_up_to(5) == [2, 3, 5]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    
    # Test that all returned numbers are actually prime
    for n in [10, 20, 30, 50, 100]:
        primes = primes_up_to(n)
        for p in primes:
            assert p <= n, f"Prime {p} > n {n}"
            if p > 1:
                assert all(p % i != 0 for i in range(2, int(p**0.5) + 1)), f"{p} is not prime"
    
    print("All edge case tests passed!")

def test_slice_bug():
    """Test for the specific slice assignment bug"""
    from sieve import primes_up_to
    
    # This should expose the slice bug if it exists
    result = primes_up_to(100)
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    if result != expected:
        print(f"Bug found! Got {len(result)} primes, expected {len(expected)}")
        print(f"Missing primes: {set(expected) - set(result)}")
        print(f"Extra primes: {set(result) - set(expected)}")
        return False
    
    return True

if __name__ == "__main__":
    test_edge_cases()
    if not test_slice_bug():
        print("Slice bug detected!")
        exit(1)
    else:
        print("No slice bugs found!")
