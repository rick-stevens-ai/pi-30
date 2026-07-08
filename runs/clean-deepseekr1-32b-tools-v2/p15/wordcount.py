def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """
    Return the top k most frequent words in the text.
    Words are lowercased and split on whitespace. Sort by frequency descending,
    then alphabetically ascending for ties.

    Args:
        text (str): Input text to analyze
        k (int): Number of top items to return

    Returns:
        list[tuple[str, int]]: List of tuples containing (word, count)

    Raises:
        ValueError: If k is non-positive or not an integer
        TypeError: If inputs are not correct type
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer")

    words = [word.lower() for word in text.split()]
    from collections import Counter
    word_counts = list(Counter(words).items())
    word_counts.sort(key=lambda x: (-x[1], x[0]))
    return word_counts[:k]

__all__ = ['top_k']