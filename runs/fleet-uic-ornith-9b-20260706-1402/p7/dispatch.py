from work.csv.backend import parse as csv_parse
from work.kv.backend import parse as kv_parse
from work.json.backend import parse as json_parse


def dispatch(kind: str, text: str) -> dict:
    if kind == "csv":
        return csv_parse(text)
    elif kind == "kv":
        return kv_parse(text)
    elif kind == "json":
        return json_parse(text)
    raise ValueError(f"Unknown backend: {kind}")
