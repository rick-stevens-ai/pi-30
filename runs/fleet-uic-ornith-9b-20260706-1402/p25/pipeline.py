from importlib.machinery import SourceFileLoader

_clean_mod = SourceFileLoader("work.clean.stage", "work/clean/stage.py").load_module()
_agg_mod = SourceFileLoader("work.agg.stage", "work/agg/stage.py").load_module()
_fmt_mod = SourceFileLoader("work.fmt.stage", "work/fmt/stage.py").load_module()


def clean(rows):
    return _clean_mod.clean(rows)


def agg(nums):
    return _agg_mod.agg(nums)


def fmt(d):
    return _fmt_mod.fmt(d)


def run(rows):
    return fmt(agg(clean(rows)))
