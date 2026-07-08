"""Integrator codec: round_trip(fmt, obj) -> loads(dumps(obj))."""

from work.csv.backend import dumps as csv_dumps, loads as csv_loads
from work.kv.backend import dumps as kv_dumps, loads as kv_loads
from work.pylit.backend import dumps as pylit_dumps, loads as pylit_loads


def round_trip(fmt, obj):
    if fmt == "csv":
        return csv_loads(csv_dumps(obj))
    elif fmt == "kv":
        return kv_loads(kv_dumps(obj))
    elif fmt == "pylit":
        return pylit_loads(pylit_dumps(obj))
    else:
        raise ValueError(f"unknown format: {fmt!r}")
