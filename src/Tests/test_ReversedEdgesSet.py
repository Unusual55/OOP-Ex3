from unittest import TestCase
from Objects.ReversedEdgesSet import ReversedEdgesSet


class TestReversedEdgesSet(TestCase):
    def test_add_edge(self):
        s = ReversedEdgesSet()
        s.add_edge(1)
        self.assertTrue(1 in s.set)
        self.assertFalse("Happy Elevator Test" in s.set)

    def test_remove_edge(self):
        s = ReversedEdgesSet()
        s.add_edge(1)
        self.assertTrue(1 in s.set)
        s.remove_edge(1)
        self.assertTrue(1 not in s.set)

    def test_contains_edge(self):
        s = ReversedEdgesSet()
        s.add_edge(1)
        self.assertEqual(True, s.contains_edge(1))
        self.assertFalse(s.contains_edge(12))

    def test_get_keys(self):
        s = ReversedEdgesSet()
        s.add_edge(1)
        s.add_edge(2)
        s.add_edge(65)
        tup = (1, 2, 65)
        actual = s.get_keys()
        for t in tup:
            self.assertEqual(True, t in actual)

    def test_clear_set(self):
        s = ReversedEdgesSet()
        s.add_edge(1)
        s.add_edge(2)
        s.add_edge(65)
        self.assertEqual(3, len(s))
        s.clear_set()
        self.assertEqual(0, len(s))

    def test_len_test(self):
        s = ReversedEdgesSet()
        self.assertEqual(0, len(s))
        s.add_edge(1)
        self.assertEqual(1, len(s))
        s.add_edge(2)
        self.assertEqual(2, len(s))
        s.add_edge(65)
        self.assertEqual(3, len(s))
        s.remove_edge(2)
        self.assertEqual(2, len(s))