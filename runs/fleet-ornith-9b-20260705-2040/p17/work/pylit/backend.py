"""Three serializer backends: csv, kv, pylit."""


def _csv_dumps(obj):
    """obj is {'fields': [...]}; returns 'a,b,c'."""
    return ",".join(str(f) for f in obj["fields"])


def _csv_loads(s):
    """Loads 'a,b,c' -> {'fields': [a, b, c]}."""
    fields = s.split(",") if s else []
    out = []
    for f in fields:
        try:
            out.append(int(f))
        except ValueError:
            try:
                out.append(float(f))
            except ValueError:
                out.append(f)
    return {"fields": out}


def _kv_dumps(obj):
    """obj is a flat {str:str}; returns 'k1=v1;k2=v2'."""
    pairs = []
    for k, v in obj.items():
        # Values are always strings in this format.
        pairs.append(f"{k}={v}")
    return ";".join(pairs)


def _kv_loads(s):
    """Loads 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}."""
    if not s:
        return {}
    result = {}
    for part in s.split(";"):
        key, _, value = part.partition("=")
        result[key] = value
    return result


def _pylit_dumps(obj):
    """Any python literal -> repr(obj)."""
    import ast

    return repr(obj)


def _pylit_loads(s):
    """Loads repr string via ast.literal_eval (stdlib only, never eval)."""
    import ast

    return ast.literal_eval(s)


# Public API: registry keyed by format name.
_backends = {
    "csv": {"dumps": _csv_dumps, "loads": _csv_loads},
    "kv": {"dumps": _kv_dumps, "loads": _kv_loads},
    "pylit": {"dumps": _pylit_dumps, "loads": _pylit_loads},
}


def dumps(fmt, obj):
    """Serialize *obj* using the named backend; returns str."""
    return _backends[fmt]["dumps"](obj)


def loads(fmt, s):
    """Deserialize *s* using the named backend; returns obj."""
    return _backends[fmt]["loads"](s)
