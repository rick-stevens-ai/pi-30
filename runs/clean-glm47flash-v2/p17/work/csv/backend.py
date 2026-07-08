def dumps(obj):
    fields = obj.get("fields", [])
    return ",".join(str(v) if v is not None else "" for v in fields)

def loads(s):
    parts = [p.strip() or "__NULL__" * len(p.split("=")[0])  # dummy restore
             .replace("__nullval=", "")*10000]