import unittest
from levenshtein import levenshtein

class TestLevenshtein(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(levenshtein("", ""), 0)
        self.assertEqual(levenshtein("abc", ""), 3)
        self.assertEqual(levenshtein("", "abc"), 3)

    def test_identical_strings(self):
        self.assertEqual(levenshtein("abc", "abc"), 0)
        self.assertEqual(levenshtein("a", "a"), 0)

    def test_single_character_diff(self):
        self.assertEqual(levenshtein("abc", "axc"), 1) # Substitution
        self.assertEqual(levenshtein("abc", "ab"), 1)  # Deletion
        self.assertEqual(levenshtein("abc", "abcd"), 1) # Insertion

    def test_completely_different(self):
        self.assertEqual(levenshtein("abc", "def"), 3)
        self.assertEqual(levenshtein("kitten", "sitting"), 3)

    def test_varying_lengths(self):
        self.assertEqual(levenshtein("flaw", "lawn"), 2)
        self.assertEqual(levenshtein("intention", "execution"), 5)
        self.assertEqual(levenshtein("gumbo", "gambol"), 2)

    def test_complex_cases(self):
        self.assertEqual(levenshtein("Saturday", "Sunday"), 3)
        self.assertEqual(levenshtein("book", "back"), 2)
        self.assertEqual(levenshtein("martha", "marhta"), 2)

    def test_unicode(self):
        self.assertEqual(levenshtein("😀😎", "😀"), 1)
        self.assertEqual(levenshtein("こんにちは", "こにちは"), 1)

if __name__ == "__main__":
    unittest.main()
