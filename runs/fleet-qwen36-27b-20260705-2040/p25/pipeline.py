import importlib.util
import os

def _import_stage(rel_dir):
    """Import a stage.py module from a relative directory."""
    path = os.path.join(os.path.dirname(__file__), rel_dir, "stage.py")
    spec = importlib.util.spec_from_file_location(rel_dir.replace("/", "."), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

clean_mod = _import_stage("work/clean")
agg_mod = _import_stage("work/agg")
fmt_mod = _import_stage("work/fmt")

clean = clean_mod.clean
agg = agg_mod.agg
fmt = fmt_mod.fmt


def run(rows):
    return fmt(agg(clean(rows)))
