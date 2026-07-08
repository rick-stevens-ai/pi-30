import unittest
from lru import LRUCache

class TestLRUCache(unittest.TestCase):
    def test_get_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(2), 2)

    def test_get_missing_key(self):
        cache = LRUCache(2)
        self.assertIsNone(cache.get(1))

    def test_put_new_key(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(len(cache.cache), 2)

    def test_put_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(1, 3)
        self.assertEqual(cache.get(1), 3)

    def test_eviction(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(3), 3)

if __name__ == '__main__':
    unittest.main()