"""CSV backend serializer.

csv: obj {"fields":[...]} <-> "a,b,c"
"""

import csv
from io import StringIO


def dumps(obj):
    """Serialize obj {"fields":[...]} to "a,b,c"."""
    fields = obj["fields"]
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(fields)
    return output.getvalue().rstrip('\r\n')


def loads(s):
    """Deserialize "a,b,c" to obj {"fields":[...]}."""
    reader = csv.reader([s])
    fields = next(reader)
    return {"fields": fields}