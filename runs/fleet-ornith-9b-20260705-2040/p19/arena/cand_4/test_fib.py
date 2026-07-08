from fib import fib

# Basic correctness checks
assert fib(0) == 0, f"fib(0)={fib(0)}"
assert fib(1) == 1, f"fib(1)={fib(1)}"
assert fib(2) == 1
assert fib(10) == 55, f"fib(10)={fib(10)}"
assert fib(50) == 12586269025

# Speed test at n=200000
import time
t = time.time()
r = fib(200_000)
print(f"fib(200000) digits: {len(str(r))}")
print(f"time: {(time.time()-t)*1e3:.2f} ms")

# Print first 50 digits as sanity check
print(f"First 50 digits: {str(r)[:50]}...")
print("OK — all checks passed.")
