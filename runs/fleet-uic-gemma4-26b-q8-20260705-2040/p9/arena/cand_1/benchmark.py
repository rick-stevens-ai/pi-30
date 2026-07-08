import time
from levenshtein import levenshtein

def benchmark():
    s1 = "a" * 1000
    s2 = "b" * 1000
    
    start = time.time()
    for _ in range(10):
        levenshtein(s1, s2)
    end = time.time()
    print(f"Time for 10 calls (1000x1000): {end - start:.4f}s")

    s3 = "abcdefg" * 100
    s4 = "abcdegh" * 100
    start = time.time()
    for _ in range(10):
        levenshtein(s3, s4)
    end = time.time()
    print(f"Time for 10 calls (700x700 with prefix/suffix): {end - start:.4f}s")

benchmark()
