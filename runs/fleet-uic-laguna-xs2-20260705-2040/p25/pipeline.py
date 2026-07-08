from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Run the 3-stage stats pipeline.
    
    Args:
        rows: Iterable of elements to process
        
    Returns:
        str: Formatted statistics string
    """
    return fmt(agg(clean(rows)))