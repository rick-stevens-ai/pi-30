from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Run the 3-stage pipeline: fmt(agg(clean(rows)))."""
    return fmt(agg(clean(rows)))