"""P25 stats pipeline integrator.

Exposes run(rows) -> fmt(agg(clean(rows))).
Each stage is a worker module under work/{clean,agg,fmt}/stage.py.
"""

from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Run the clean -> agg -> fmt pipeline and return the formatted string."""
    return fmt(agg(clean(rows)))