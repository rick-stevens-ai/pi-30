import decimal
_orig_Decimal = decimal.Decimal
class _PatchedDecimal(_orig_Decimal):
    def __sub__(self, other):
        if isinstance(other, float):
            return _orig_Decimal.__sub__(self, _orig_Decimal(other))
        return _orig_Decimal.__sub__(self, other)

decimal.Decimal = _PatchedDecimal

x = decimal.Decimal(1.0)
print(type(x))
print(x - 0.5)
PY