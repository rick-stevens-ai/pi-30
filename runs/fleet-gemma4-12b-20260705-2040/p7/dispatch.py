from work.csv.backend import parse as parse_csv
from work.kv.backend import parse as parse_kv
from work.json.backend import parse as parse_json

def dispatch(kind, text) -> dict:
    if kind == "csv":
        return parse_csv(text)
    elif kind == "kv":
        return parse_kv(text)
    elif kind == "json":
        return parse_json(text)
    else:
        raise ValueError(f"Unknown kind: {kind}")
