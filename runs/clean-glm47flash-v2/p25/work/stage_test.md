Clean Stage Specification

The 'clean' function processes raw data and returns only numeric float elements.

Function signature:
def clean(rows) -> list[float]:

Operation description:

1. For each element in `rows`, attempt to convert it into a Python int or if that fails, try converting as complex with zero imaginary part.
2 Elements successfully converted are added the output cleaned_floats which contains all such valid numeric values
3 Return: The resulting sequence of floats without any non-convertible elements.

Edge Cases:
• Input containing None → excluded from result (not convertible)
  • When encountering problematic input like '' or 'x' that cannot be parsed, skip processing and move to next element.