from work.csv.backend import parse as csv_parse
from work.kv.backend import parse as kv_parse
from work.json.backend import parse as json_parse

def dispatch(kind, text):
    """
    Routes parsing requests based on kind to the appropriate backend.

    Args:
        kind (str): The type of data ('csv', 'kv', or 'json').
        text (str): The input text to be parsed.

    Returns:
        dict: The parsed dictionary, or raises an error if kind is unknown.
    """
    if kind == 'csv':
        return csv_parse(text)
    elif kind == 'kv':
        return kv_parse(text)
    elif kind == 'json':
        return json_parse(text)
    else:
        raise ValueError(f"Unknown data kind: {kind}. Must be one of ['csv', 'kv', 'json'].")

if __name__ == '__main__':
    # Example usage (for testing purposes, though not strictly required by the prompt)
    try:
        print("Testing CSV:")
        result_csv = dispatch('csv', "header1,header2\nvalue1,value2")
        print(f"CSV Result: {result_csv}")

        print("\nTesting JSON:")
        result_json = dispatch('json', '{"key": "value"}')
        print(f"JSON Result: {result_json}")

    except Exception as e:
        print(f"An error occurred during test execution: {e}")