from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Pipeline: drop non-numeric, aggregate stats, format string."""
    return fmt(agg(clean(rows)))
