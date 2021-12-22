import random
from Objects.Edge import Edge
from Objects.Node import Node
from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph


class GraphObjectsGenerator:
    def __init__(self):
        self.val = None

    def is_finished(self, outdegree: list, indegree: list):
        for i in range(len(outdegree)):
            if outdegree[i] > 0 and indegree[i] > 0:
                return False
        return True

    def generate_nodes(self, count: int):
        nodes = []
        for i in range(count):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            z = random.uniform(0, 10)
            n = Node(i, x, y, z)
            nodes.append(n)
        return nodes

    def generate_empty_nodes(self, count: int):
        nodes = []
        for i in range(count):
            nodes.append((None, None, None))
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

    def generate_large_graph(self, nodecount: int):
        nodes = self.generate_nodes(nodecount)
        edges = set()
        indegree = []
        outdegree = []
        for i in range(nodecount):
            inrank = random.randint(4, 10)
            outrank = 20 - inrank
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