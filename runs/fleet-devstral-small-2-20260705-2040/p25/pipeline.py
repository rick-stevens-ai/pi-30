from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Run the full pipeline: clean -> agg -> fmt.
    
    Args:
        rows: List of rows where each row is a list of elements
        
    Returns:
        Formatted string with aggregation statistics
    """
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted
