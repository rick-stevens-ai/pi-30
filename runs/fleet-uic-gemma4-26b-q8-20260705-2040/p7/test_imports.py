try:
    from work.kv.backend import parse as kv_parse
    print("Successfully imported kv_parse")
except ImportError as e:
    print(f"Failed to import kv_parse: {e}")

try:
    from work.json.backend import parse as json_parse
    print("Successfully imported json_parse")
except ImportError as e:
    print(f"Failed to import json_parse: {e}")

try:
    # This is the weird one
    from work.csv.work.csv.backend import parse as csv_parse
    print("Successfully imported csv_parse")
except ImportError as e:
    print(f"Failed to import csv_parse: {e}")

