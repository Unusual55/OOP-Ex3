import random
from unittest import TestCase
from Objects.Node import Node


class TestNode(TestCase):
    def test_get_key(self):
        nodes = []
        for i in range(20):
            nodes.append(Node(i))
        for i in range(20):
            self.assertEquals(i, nodes[i].getKey())

    def test_checkpos(self):
        nodes = []
        for i in range(20):
            if i % 2 == 0:
                nodes.append(Node(i))
            else:
                n = Node(i)
                n.setlimitedrandompos(0, 0, 0, 10, 10, 10)
                nodes.append(n)
        for i in range(20):
            if i % 2 == 0:
                self.assertEqual(False, nodes[i].checkpos())
            else:
                self.assertEqual(True, nodes[i].checkpos())

    def test_getters(self):
        nodes = []
        for i in range(20):
            if i % 2 == 0:
                nodes.append(Node(i))
            else:
                n = Node(i)
                n.setlimitedrandompos(0, 0, 0, 10, 10, 10)
                nodes.append(n)
        for i in range(20):
            if not nodes[i].checkpos():
                self.assertEquals((None, None, None), nodes[i].getpos())
            else:
                ni = nodes[i]
                tup = (ni.x, ni.y, ni.z)
                self.assertEquals(tup, nodes[i].getpos())
                self.assertEquals(tup[0], nodes[i].get_x())
                self.assertEquals(tup[1], nodes[i].get_y())
                self.assertEquals(tup[2], nodes[i].get_z())

    def test_setpos(self):
        n = Node(0)
        self.assertEquals(False, n.checkpos())
        n.setpos(1, 3, 6)
        self.assertEquals(True, n.checkpos())
        self.assertEquals((1, 3, 6), n.getpos())

    def test_setlimitedrandompos(self):

        n = Node(0)
        self.assertEquals(False, n.checkpos())
        n.setlimitedrandompos(0, 0, 0, 10, 10, 10)
        self.assertEquals(True, n.checkpos())

    def test_distance(self):
        nodes = []
        for i in range(20):
            n = Node(i)
            n.setlimitedrandompos(0, 0, 0, 10, 10, 10)
            nodes.append(n)
        for i in range(20):
            for j in range(i, 20):
                dx = (nodes[i].x - nodes[j].x) ** 2
                dy = (nodes[i].y - nodes[j].y) ** 2
                dz = (nodes[i].z - nodes[j].z) ** 2
                from math import sqrt
                self.assertEqual(sqrt(dx + dy + dz), nodes[i].distance(nodes[j]))

    def test_str(self):
        n = Node(0, 1.0, 2.5, 3.0)
        self.assertEquals("(0): (1.0, 2.5, 3.0)", n.__str__())

    def test_eq(self):
        n = Node(0, float(1.0), float(2.5), float(3.0))
        ncop = Node(0, 1.0, 2.5, 3.0)
        self.assertEqual(True, n.__eq__(ncop))
        self.assertEqual(False, n.__eq__(ncop.setlimitedrandompos(0, 0, 0, 10, 10, 10)))
