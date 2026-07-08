b = bytearray([1]) * 4
print(f"Length of b: {len(b)}")
try:
    b[4::3] = bytes([0]) * ((4 - 1 - 4) // 3 + 1)
    print("Success")
except IndexError as e:
    print(f"IndexError: {e}")
