"""CSV backend:  obj = {"fields": [...]} <-> "a,b,c"  (stdlib only)."""

import csv as _csv
import io


def dumps(obj):
    fields = obj["fields"]
    buf = io.StringIO()
    writer = _csv.writer(buf, quoting=_csv.QUOTE_MINIMAL)
    writer.writerow(fields)
    return buf.getvalue().rstrip("\r\n")


def loads(s):
    if not s:
        return {"fields": []}
    reader = _csv.reader(io.StringIO(s))
    values = next(reader)
    return {"fields": list(values)}
