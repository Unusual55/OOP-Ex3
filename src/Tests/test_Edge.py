import random
from unittest import TestCase
from Objects.Edge import Edge


class TestEdge(TestCase):
    def test_getters(self):
        for i in range(20):
            for j in range(20):
                if i == j:
                    continue
                w = random.uniform(0, 5)
                src = i
                dest = j
                e = Edge(src, dest, w)
                self.assertEqual(src, e.get_src())
                self.assertEqual(dest, e.get_dest())
                self.assertEqual(w, e.get_weight())

    def test_set_weight(self):
        for i in range(20):
            for j in range(20):
                if i == j:
                    continue
                w = random.uniform(0, 5)
                src = i
                dest = j
                e = Edge(src, dest, w)
                self.assertEqual(w, e.get_weight())
                w = random.uniform(0, 5)
                self.assertNotEqual(w, e.get_weight())
                e.set_weight(w)
                self.assertEqual(w, e.get_weight())

    def test_str_test(self):
        e = Edge(1, 6, 800.65)
        expected = "(1-> 6): 800.65"
        self.assertEqual(expected, e.__str__())

    def test_eq_test(self):
        edges = []
        for i in range(20):
            for j in range(20):
                if i == j:
                    continue
                w = random.uniform(0, 5)
                e = Edge(i, j, w)
                edges.append(e)
        for i in range(20):
            for j in range(20):
                if i == j:
                    continue
                b1 = edges[i].get_src() == edges[j].get_src()
                b2 = edges[i].get_dest() == edges[j].get_dest()
                b3 = edges[i].get_weight() == edges[j].get_weight()
                self.assertEqual(b1 and b2 and b3, edges[i].__eq__(edges[j]))