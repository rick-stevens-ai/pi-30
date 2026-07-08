import decimal
from decimal import Decimal

def test_monkeypatch():
    try:
        d = Decimal('1.0')
        f = 0.5
        print(f"Original subtraction:")
        print(d - f)
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Try to monkeypatch __sub__
    # We need to see if it's possible.
    try:
        Decimal.__sub__ = lambda self, other: Decimal(str(self)) - Decimal(str(other))
        d = Decimal('1.0')
        f = 0.5
        print(f"Monkeypatched subtraction:")
        print(d - f)
    except Exception as e:
        print(f"Failed to monkeypatch: {e}")

if __name__ == "__main__":
    test_monkeypatch()
