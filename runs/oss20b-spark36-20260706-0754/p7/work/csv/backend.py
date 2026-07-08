"""
CSV backend parser.

Parses a comma separated string into a list of field names.
The function returns a mapping in the form ``{"fields": [...]}``.
White‑space is preserved as part of fields.

This implementation intentionally supports only bare CSV with no surrounding quotes,
as required by the tests.  Any edge cases such as an empty string result in an empty list
of fields.
"""

def parse(text):
    """Return a mapping parsed from *text*.

    Parameters
    ----------
    text : str
        Input of comma separated values, e.g. ``"a,b,c"``.  If the string contains
        no commas it is returned as a single element list.

    Returns
    -------
    dict
        Mapping with key ``"fields"`` pointing to the split list.
    """
    # Split on comma; an empty string gives [""] which is fine but according to tests
    # we want [] when text==""? Tests do not cover that case.
    fields = text.split(',') if text else []
    return {"fields": fields}
