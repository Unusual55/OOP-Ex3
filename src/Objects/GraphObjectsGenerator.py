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
            if (outdegree[i] > 0) and (indegree[i] > 0):
                return False
        return True

    def generate_nodes(self, count: int):
        return [Node(i, random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)) for i in range(count)]

    def generate_empty_nodes(self, count: int):
        return [(None, None, None)] * count

    def generate_graph(self, nodecount: int, avgdegree: int):
        nodes = self.generate_nodes(nodecount)
        edges = set()
        indegree = [random.randint(2, 5) for _ in range(nodecount)]
        outdegree = [10 - i for i in indegree]
        flag = False
        while not flag:
            src = random.randint(0, nodecount - 1)
            dest = random.randint(0, nodecount - 1)
            failedsrc = set()
            while (outdegree[src] == 0) and (len(failedsrc) <= nodecount - 1):
                failedsrc.add(src)
                src = random.randint(0, nodecount - 1)
                if src in failedsrc:
                    continue
            faileddest = set()
            while (indegree[dest] == 0) and (len(faileddest) <= nodecount - 1):
                faileddest.add(dest)
                dest = random.randint(0, nodecount - 1)
                if (dest in faileddest) or (src == dest):
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
        indegree = [random.randint(4, 10) for _ in range(nodecount)]
        outdegree = [20 - i for i in indegree]
        flag = False
        while not flag:
            src = random.randint(0, nodecount - 1)
            dest = random.randint(0, nodecount - 1)
            failedsrc = set()
            while (outdegree[src] == 0) and (len(failedsrc) <= nodecount - 1):
                failedsrc.add(src)
                src = random.randint(0, nodecount - 1)
                if src in failedsrc:
                    continue
            faileddest = set()
            while (indegree[dest] == 0) and (len(faileddest) <= nodecount - 1):
                faileddest.add(dest)
                dest = random.randint(0, nodecount - 1)
                if (dest in faileddest) or (src == dest):
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
