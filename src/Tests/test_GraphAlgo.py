from unittest import TestCase
# from Objects.Edge import Edge
# from Objects.Node import Node
# from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph
from Objects.GraphAlgo import GraphAlgo
# import _heapq
# from api.GraphInterface import GraphInterface
# from api.GraphAlgoInterface import GraphAlgoInterface
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
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\my_graph.json")

    def test_shortest_path(self):
        g = DiGraph()
        g.add_node(0, (0.0, 0.0, 0.0))
        g.add_node(1, (1.0, 1.0, 1.0))
        g.add_node(2, (2.0, 2.0, 2.0))
        g.add_node(3, (3.6, 3.5, 3.75))
        g.add_edge(0, 1, 1.2)
        g.add_edge(1, 0, 1.4)
        g.add_edge(1, 2, 1.5)
        g.add_edge(2, 1, 2.0)
        g.add_edge(0, 3, 0.3)
        g.add_edge(3, 2, 0.7)
        ga = GraphAlgo(g)
        ga.shortest_path(0, 2)
        self.assertEqual((1.0, [0, 3, 2]), ga.shortest_path(0, 2))
        ga.dijkstra(0)

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

    def test_center_point(self):
        ga = GraphAlgo()
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A0.json")
        print("A0: " + str(ga.centerPoint()))
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A1.json")
        print("A1: " + str(ga.centerPoint()))
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A2.json")
        print("A2: " + str(ga.centerPoint()))
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A3.json")
        print("A3: " + str(ga.centerPoint()))
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A4.json")
        print("A4: " + str(ga.centerPoint()))
        ga.load_from_json("C:\\Users\\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\\Data\\A5.json")
        print("A5: " + str(ga.centerPoint()))

    def test_TSP(self):
        ga = GraphAlgo()
        ga.load_from_json("C:\\Users\ofrit\\PycharmProjects\\Ex3\\OOP-Ex3\\src\Data\\1000Nodes.json")
        l = [931, 179, 77, 167, 252, 964, 960, 513, 316, 700, 495, 658, 11, 200, 152, 719, 585, 140]
        out = ga.TSP(l)
        self.assertEqual(10408.402683188457, out[1])
        print(out)
