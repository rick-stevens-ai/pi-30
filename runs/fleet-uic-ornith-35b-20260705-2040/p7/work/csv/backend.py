"""CSV backend — parses a single CSV line into {"fields": [...]}. Stdlib only."""
import csv
import io


def parse(text: str) -> dict:
    """Parse a single CSV line/text and return {"fields": ["a", "b", ...]}."""
    reader = csv.reader(io.StringIO(text))
    for row in reader:
        break  # we only ever expect one row / line

    if not isinstance(row, list):
        raise ValueError(f"csv.parse expected a sequence, got {type(row).__name__}")
    for i, field in enumerate(row):
        if not isinstance(field, str):
            raise TypeError(
                f"field[{i}] must be str (instance of {type(field).__name__})"
            )

    return {"fields": list(row)}
