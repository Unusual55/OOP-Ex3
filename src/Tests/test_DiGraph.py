import random
from unittest import TestCase
from Objects.Edge import Edge
from Objects.Node import Node
from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph


class TestDiGraph(TestCase):
    def generate_nodes(self, count: int):
        nodes = []
        for i in range(count):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            z = random.uniform(0, 10)
            n = Node(i, x, y, z)
            nodes.append(n)
        return nodes

    def generate_graph(self, nodecount: int, avgdegree: int):
        nodes = self.generate_nodes(nodecount)
        edges = set()
        indegree = []
        outdegree = []
        for i in range(nodecount):
            inrank = random.randint(2, 5)
            outrank = 10 - inrank
            indegree.append(inrank)
            outdegree.append(outrank)
        flag = False
        while not flag:
            src = random.randint(0, nodecount - 1)
            dest = random.randint(0, nodecount - 1)
            failedsrc = set()
            while outdegree[src] == 0 and len(failedsrc) <= nodecount - 1:
                failedsrc.add(src)
                src = random.randint(0, nodecount - 1)
                if src in failedsrc:
                    continue
            faileddest = set()
            while indegree[dest] == 0 and len(faileddest) <= nodecount - 1:
                faileddest.add(dest)
                dest = random.randint(0, nodecount - 1)
                if dest in faileddest or src == dest:
                    continue
                continue
            e = Edge(src, dest, nodes[src].distance(nodes[dest]))
            edges.add(e)
            outdegree[src] -= 1
            indegree[dest] -= 1
            if self.is_finished(outdegree, indegree):
                flag = True
        g = DiGraph()
        for node in nodes:
            g.add_node(node.getKey(), node.getpos())
        for edge in edges:
            g.add_edge(edge.src, edge.dest, edge.w)
        return g

    def is_finished(self, outdegree: list, indegree: list):
        for i in range(len(outdegree)):
            if outdegree[i] > 0 and indegree[i] > 0:
                return False
        return True

    def test_v_size(self):
        g = DiGraph()
        nodes = self.generate_nodes(20)
        for i in nodes:
            g.add_node(i.getKey(), i.getpos())
        self.assertEqual(20, g.v_size())

    def test_e_size(self):
        g = DiGraph()
        nodes = self.generate_nodes(5)
        for n in nodes:
            g.add_node(n.getKey(), n.getpos())
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                e = Edge(i, j, nodes[i].distance(nodes[j]))
                g.add_edge(i, j, e.get_weight())
        self.assertEqual(20, g.e_size())

    def test_get_mc(self):
        g = DiGraph()
        nodes = self.generate_nodes(5)
        for n in nodes:
            g.add_node(n.getKey(), n.getpos())
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                e = Edge(i, j, nodes[i].distance(nodes[j]))
                g.add_edge(i, j, e.get_weight())
        self.assertEqual(25, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()
        nodes = self.generate_nodes(5)
        for n in nodes:
            g.add_node(n.getKey(), n.getpos())
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                e = Edge(i, j, nodes[i].distance(nodes[j]))
                g.add_edge(i, j, e.get_weight())
        self.assertEqual(20, g.e_size())

    def test_add_node(self):
        g = DiGraph()
        nodes = self.generate_nodes(20)
        for i in nodes:
            g.add_node(i.getKey(), i.getpos())
        self.assertEqual(20, g.v_size())

    def test_remove_node(self):
        g = self.generate_graph(20, 10)
        indegree = len(g.inEdges.get(0, ReversedEdgesSet))
        outdegree = len(g.outEdges.get(0, {}).keys())
        preedgecount = g.e_size()
        prenodecount = g.v_size()
        premc = g.get_mc()
        g.remove_node(0)
        self.assertNotEqual(preedgecount, g.e_size())

    def test_remove_edge(self):
        g = DiGraph()
        g.add_node(0, (1.2, 2.11, 5.5453))
        g.add_node(1, (4.9999, 6.2, 8.0))
        g.add_edge(0, 1, 2)
        self.assertEqual(1, g.e_size())
        g.remove_edge(0, 1)
        self.assertEqual(0, g.e_size())

    def test_get_all_v(self):
        nodes = set(self.generate_nodes(20))
        g = DiGraph()
        for node in nodes:
            g.add_node(node.getKey(), node.getpos())
        vdict = g.get_all_v()
        for v in vdict.values():
            self.assertTrue(v in nodes)

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        g.add_node(0, (1.2, 2.11, 5.5453))
        g.add_node(1, (4.9999, 6.2, 8.0))
        g.add_node(2, (4.4543, 2.243, 4454.3))
        g.add_edge(0, 1, 2)
        g.add_edge(2, 1, 4)
        self.assertEqual(2, g.e_size())
        edges = dict()
        edges[0] = 2
        edges[2] = 4
        indict = g.all_in_edges_of_node(1)
        for v in indict:
            self.assertTrue(v in edges)

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        g.add_node(0, (1.2, 2.11, 5.5453))
        g.add_node(1, (4.9999, 6.2, 8.0))
        g.add_node(2, (4.4543, 2.243, 4454.3))
        g.add_edge(0, 1, 2)
        g.add_edge(0, 2, 4)
        self.assertEqual(2, g.e_size())
        edges = dict()
        edges[1] = 2
        edges[2] = 4
        outdict = g.all_out_edges_of_node(0)
        for v in outdict:
            self.assertTrue(v in edges)
