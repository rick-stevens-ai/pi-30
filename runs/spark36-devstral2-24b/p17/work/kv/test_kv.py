#!/usr/bin/env python3
"""
Quick sanity test forkv backend.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import dumps, loads

def test_empty():
    obj = {}
    s = dumps(obj)
    roundtrip = loads(s)
    assert s == "", f"Expected empty string, got '{s}'"
    assert roundtrip == {}, f"Expected empty dict, got {roundtrip}"

def test_simple():
    obj = {"a": "1", "b": "2"}
    s = dumps(obj)
    expected = "a=1;b=2"
    assert s == expected, f"Expected '{expected}', got '{s}'"
    roundtrip = loads(s)
    assert roundtrip == obj, f"Expected {obj}, got {roundtrip}"

def test_with_special_chars():
    # Test with semicolon and equals in values
    obj = {"key1": "value;with;semicolons", "key2": "equals=in=value"}
    s = dumps(obj)
    roundtrip = loads(s)
    assert roundtrip == obj, f"Expected {obj}, got {roundtrip}"

if __name__ == "__main__":
    test_empty()
    test_simple()
    test_with_special_chars()
    print("All kv backend tests passed!")
