"""csv backend: {"fields":[...]} <-> "a,b,c" using stdlib csv only."""
import csv
import io

def dumps(obj):
    """Serialize {"fields":[...]} to a comma-separated row string."""
    fields = obj["fields"]
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow([str(f) for f in fields])
    return out.getvalue().rstrip("\r\n")

def loads(s):
    """Deserialize a comma-separated row string to {"fields":[...]}."""
    reader = csv.reader(io.StringIO(s))
    fields = next(reader)
    return {"fields": fields}