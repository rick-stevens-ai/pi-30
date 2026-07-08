'''Pipeline integrating the three stages.

The pipeline imports the `clean`, `agg`, and `fmt` functions from their
respective modules under ``work/*/stage.py`` and defines a single public
function ``run`` that applies them in order.
'''  # noqa: D400

# Import statements – each stage resides in its own package under ``work``.
# The ``stage.py`` modules define ``__all__`` so we can import the function
# directly.
from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Run the stats pipeline.

    Parameters
    ----------
    rows : iterable
        Raw input rows – typically strings but any object accepted by the
        ``clean`` stage.

    Returns
    -------
    str
        Formatted statistics string produced by the ``fmt`` stage.
    """
    # Apply the stages in the required order.
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted