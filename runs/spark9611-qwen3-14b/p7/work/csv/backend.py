import csv

def parse(text, format):
    if format == 'csv':
        reader = csv.reader([text])
        fields = next(reader)
        return {'fields': fields}
    else:
        raise ValueError(f"Unsupported format: {format}")