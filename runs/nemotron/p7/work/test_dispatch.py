"""Tests for the dispatch module."""
import pytest
from dispatch import parse, available_formats


def test_available_formats():
    assert set(available_formats()) == {"csv", "json", "kv"}


def test_parse_csv():
    result = parse("csv", "a,b,c")
    assert result == {"fields": ["a", "b", "c"]}

    result = parse("csv", "")
    assert result == {"fields": []}


def test_parse_json():
    result = parse("json", '{"a": 1, "b": 2}')
    assert result == {"a": 1, "b": 2}

    result = parse("json", "{}")
    assert result == {}


def test_parse_kv():
    result = parse("kv", "k1=v1;k2=v2")
    assert result == {"k1": "v1", "k2": "v2"}

    result = parse("kv", "")
    assert result == {}

    result = parse("kv", "a=b;c=d;e=f")
    assert result == {"a": "b", "c": "d", "e": "f"}


def test_unknown_format():
    with pytest.raises(ValueError, match="Unknown format"):
        parse("unknown", "data")

    with pytest.raises(ValueError, match="xml"):
        parse("xml", "data")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])