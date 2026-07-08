import pytest
from levenshtein import levenshtein


def test_empty_strings():
    """Test with empty strings."""
    assert levenshtein("", "") == 0
    assert levenshtein("", "abc") == 3
    assert levenshtein("abc", "") == 3


def test_identical_strings():
    """Test with identical strings."""
    assert levenshtein("hello", "hello") == 0
    assert levenshtein("abc", "abc") == 0
    assert levenshtein("", "") == 0


def test_single_character():
    """Test with single character strings."""
    assert levenshtein("a", "a") == 0
    assert levenshtein("a", "b") == 1
    assert levenshtein("a", "") == 1
    assert levenshtein("", "a") == 1


def test_simple_cases():
    """Test simple cases."""
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("saturday", "sunday") == 3
    assert levenshtein("book", "back") == 2
    assert levenshtein("abc", "def") == 3


def test_different_lengths():
    """Test strings of different lengths."""
    assert levenshtein("abc", "abcd") == 1
    assert levenshtein("abcd", "abc") == 1
    assert levenshtein("abc", "ab") == 1
    assert levenshtein("ab", "abc") == 1


def test_substitution_only():
    """Test cases requiring only substitutions."""
    assert levenshtein("abc", "adc") == 1
    assert levenshtein("abc", "abd") == 1
    assert levenshtein("abc", "abc") == 0


def test_insertion_only():
    """Test cases requiring only insertions."""
    assert levenshtein("abc", "aXbc") == 1
    assert levenshtein("abc", "aXbXc") == 2
    assert levenshtein("abc", "Xabc") == 1


def test_deletion_only():
    """Test cases requiring only deletions."""
    assert levenshtein("aXbc", "abc") == 1
    assert levenshtein("aXbXc", "abc") == 2
    assert levenshtein("Xabc", "abc") == 1


def test_mixed_operations():
    """Test cases requiring mixed operations."""
    assert levenshtein("abcdef", "azced") == 3
    assert levenshtein("programming", "gramming") == 3
    assert levenshtein("kitten", "sitting") == 3


def test_long_strings():
    """Test with longer strings."""
    assert levenshtein("hello world", "hello universe") == 7
    assert levenshtein("the quick brown fox", "the slow brown dog") == 7


def test_unicode_strings():
    """Test with unicode characters."""
    assert levenshtein("café", "cafe") == 1
    assert levenshtein("naïve", "naive") == 1
    assert levenshtein("日本語", "日本") == 1


def test_performance():
    """Test performance with large strings."""
    import time
    
    # Test with large strings
    a = "a" * 1000
    b = "b" * 1000
    
    start = time.time()
    result = levenshtein(a, b)
    end = time.time()
    
    assert result == 1000
    assert end - start < 1.0  # Should be reasonably fast


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
