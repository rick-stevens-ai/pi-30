import csv
import io


def dumps(obj: dict) -> str:
    """{"fields":[...]} -> "a,b,c" via CSV."""
    fields = obj["fields"]
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(fields)
    return buf.getvalue().rstrip("\r\n")


def loads(s: str) -> dict:
    '"a,b,c" -> {"fields":[...]}'
    reader = csv.reader(io.StringIO(s))
    rows = list(reader)
    if not rows or not rows[0]:
        fields = []
    else:
        fields = rows[0]
    return {"fields": fields}
