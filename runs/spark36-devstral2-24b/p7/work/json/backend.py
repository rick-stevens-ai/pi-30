import json

def parse(text):
    """
    Parse text into a dictionary.
    
    Format: 'json'
    Example input: '{"k1": "v1", "k2": "v2"}'
    Output: {"k1": "v1", "k2": "v2"}
    """
    return json.loads(text)
