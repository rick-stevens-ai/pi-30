def fib(n):
    if n < 0: return None
    if n == 0: return 0
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a)
        d = a * a + b * b
        a, b = c, d
        if bit == '1':
            a, b = b, a + b
    # Wait, if the first bit was 1, we moved from k=0 to k=1.
    # But my loop for n=5 (binary 101) gave index 5 at the end.
    # Let's re-trace carefully.
    return a

def fib_expected(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(f"n=0: {fib(0)} (expected 0)")
print(f"n=1: {fib(1)} (expected 1)")
print(f"n=2: {fib(2)} (expected 1)")
print(f"n=3: {fib(3)} (expected 2)")
print(f"n=4: {fib(4)} (expected 3)")
print(f"n=5: {fib(5)} (expected 5)")

for i in range(10):
    if fib(i) != fib_expected(i):
        print(f"FAIL at n={i}: got {fib(i)}, expected {fib_expected(i)}")
        break
else:
    print("All tests passed!")
