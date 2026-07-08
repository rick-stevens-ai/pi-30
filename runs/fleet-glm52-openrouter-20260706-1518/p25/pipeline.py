"""Integrator: run(rows) -> fmt(agg(clean(rows)))."""
from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """clean -> agg -> fmt."""
    return fmt(agg(clean(rows)))
