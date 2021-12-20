from unittest import TestCase
from Objects.Edge import Edge
from Objects.Node import Node
from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph
from Objects.GraphAlgo import GraphAlgo
import _heapq
from api.GraphInterface import GraphInterface
from api.GraphAlgoInterface import GraphAlgoInterface
from Objects.GraphObjectsGenerator import GraphObjectsGenerator


class TestGraphAlgo(TestCase):
    # def test_load_from_json(self):
    #     self.fail()
    #
    def test_save_to_json(self):
        gener = GraphObjectsGenerator()
        g = gener.generate_graph(20, 0)
        ga = GraphAlgo(g)
        ga.save_to_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\my_graph")
        emptynodes = gener.generate_empty_nodes(5)
        i = 0
        for empty in emptynodes:
            g.add_node(20 + i, empty)
            i += 1
        ga.g = g
        ga.save_to_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\my_NoneIncluded_graph")
        emptygraph = DiGraph()
        emptygraphnodes = gener.generate_empty_nodes(50)
        i = 0
        for e in emptygraphnodes:
            emptygraph.add_node(i, e)
            i += 1
        ga.g = emptygraph
        ga.save_to_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\my_empty_graph")


    # def test_shortest_path(self):
    #     self.fail()

    def test_get_graph(self):
        gener = GraphObjectsGenerator()
        g = gener.generate_graph(20, 0)
        ga = GraphAlgo(g)
        self.assertEqual(True, ga.get_graph().__eq__(g))

    def test_plot_graph(self):
        gener = GraphObjectsGenerator()
        g = gener.generate_graph(20, 0)
        ga = GraphAlgo(g)
        emptynodes = gener.generate_empty_nodes(5)
        i = 20
        for n in emptynodes:
            ga.g.add_node(i, n)
            i += 1
        vdict = ga.get_graph().get_all_v()
        for i in range(20, 24):
            self.assertEquals(False, vdict.get(i).checkpos())
        ga.plot_graph()
        for i in range(20, 24):
            self.assertEquals(True, vdict.get(i).checkpos())
