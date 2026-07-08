import importlib

def round_trip(fmt: str, obj):
    # The paths are unusual according to ls -R work:
    # csv -> work/csv/work/csv/backend.py
    # kv  -> work/kv/backend.py
    # pylit -> work/pylit/work/pylit/backend.py

    if fmt == "csv":
        module = importlib.import_module("work.csv.work.csv.backend")
    elif fmt == "kv":
        module = importlib.import_module("work.kv.backend")
    elif fmt == "pylit":
        module = importlib.import_module("work.pylit.work.pylit.backend")
    else:
        raise ValueError(f"Unknown format: {fmt}")

    dumps = module.dumps
    loads = module.loads

    return loads(dumps(obj))
