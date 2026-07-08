"""Codec: route round_trip(fmt, obj) to the matching backend."""

from work.csv.backend import dumps as csv_dumps, loads as csv_loads
from work.kv.backend import dumps as kv_dumps, loads as kv_loads
from work.pylit.backend import dumps as pylit_dumps, loads as pylit_loads

_DUMPS = {
    "csv": csv_dumps,
    "kv": kv_dumps,
    "pylit": pylit_dumps,
}
_LOADS = {
    "csv": csv_loads,
    "kv": kv_loads,
    "pylit": pylit_loads,
}


def round_trip(fmt, obj):
    """Serialize obj with the named backend, then load it back."""
    if fmt not in _DUMPS:
        raise ValueError("unknown format %r" % (fmt,))
    return _LOADS[fmt](_DUMPS[fmt](obj))
