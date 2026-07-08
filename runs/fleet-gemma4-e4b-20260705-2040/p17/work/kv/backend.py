from typing import Dict

def dumps(obj: Dict[str, str]) -> str:
    """
    Dumps a flat dictionary {str:str} into a semicolon-separated string 
    where key and value are separated by '='. E.g., {'k1': 'v1', 'k2': 'v2'} -> 'k1=v1;k2=v2'.
    """
    if not isinstance(obj, dict):
        raise TypeError("Input must be a dictionary.")
        
    parts = []
    for key, value in obj.items():
        # Assuming keys and values are strings as per the requirement {str:str}
        parts.append(f"{key}={value}")
    return ";".join(parts)

def loads(s: str) -> Dict[str, str]:
    """
    Loads a semicolon-separated string 'k1=v1;k2=v2' back into a flat dictionary {str:str}.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
        
    result = {}
    pairs = s.split(';')
    for pair in pairs:
        if '=' not in pair:
            # Handle cases where the segment might be empty or malformed if necessary, 
            # but for strict KV format 'k=v', we expect one '='.
            continue 
        try:
            key, value = pair.split('=', 1) # Split only on the first '=', allowing values to contain '='
            result[key] = value
        except ValueError:
            # Should not happen if split('=', 1) is used correctly, but good practice.
            continue
    return result

# Example usage (for testing/demonstration, remove if strictly adhering to API contract):
if __name__ == '__main__':
    test_obj = {"user_id": "12345", "session_key": "abcde"}
    serialized = dumps(test_obj)
    print(f"Original: {test_obj}")
    print(f"Serialized: {serialized}")

    deserialized = loads(serialized)
    print(f"Deserialized: {deserialized}")
    assert test_obj == deserialized