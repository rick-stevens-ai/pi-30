from work.csv import backend as csv_backend
from work.kv import backend as kv_backend
from work.json import backend as json_backend

BACKENDS = {
    'csv': csv_backend.parse,
    'kv': kv_backend.parse,
    'json': json_backend.parse,
}

def dispatch(kind, text):
    if kind not in BACKENDS:
        raise ValueError(f"Unsupported kind: {kind}")
    return BACKENDS[kind](text)
