import csv
import io

def dumps(obj):
    fields = obj["fields"]
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="")
    writer.writerow(fields)
    return output.getvalue()

def loads(s):
    input_stream = io.StringIO(s)
    reader = csv.reader(input_stream)
    row = next(reader)
    return {"fields": row}
