import sys
import os

print("Current working directory:", os.getcwd())
print("Python sys.path:")
for p in sys.path:
    print(f"  {p}")

try:
    import reduce
    print("reduce.__file__:", reduce.__file__)
except ImportError as e:
    print(f"ImportError: {e}")
