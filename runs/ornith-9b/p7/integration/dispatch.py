from importlib import import_module, util

import sys

MODULES = {
    "csv": util.find_spec("backend", "/run/work/csv"),
    "kv": util.find_spec("backend", "/work/kv"),
    "json": util.find_spec("backend", "/work/json"),
}


def dispatch(kind: str, text: str) -> dict:
    spec = MODULES[kind]
    mod = import_module("backend", spec if spec else None) or sys.modules[f"run.py.work.{kind}"]  # noqa
    return mod.parse(text)
