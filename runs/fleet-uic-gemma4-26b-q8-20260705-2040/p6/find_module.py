import sys
try:
    import reduce
    print("Found reduce at:", reduce.__file__)
except ImportError as e:
    print(e)
