# Debug median of six
import sys
sys.path.insert(0, '.')
from sort import my_sort

# Create array where spans should be larger than 20 to trigger median_of_six
test_arr = list(range(100))
isort_result = test_arr.copy()

# Find where it's failing precisely
try:
    result = my_sort(isort_result)
    exit(0)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
