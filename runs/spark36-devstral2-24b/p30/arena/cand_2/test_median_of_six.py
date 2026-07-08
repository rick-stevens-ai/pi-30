# Test median of six implementation
import sys
sys.path.insert(0, '.')
from sort import my_sort

# Should trigger median_of_six when we have larger arrays
big_list = list(range(100)) + [50]  # Add duplicate to test element stability
scrambled = big_list.copy()
import random
random.shuffle(scrambled)
result = my_sort(scrambled)
print("Big list sort:", result == sorted(big_list))
