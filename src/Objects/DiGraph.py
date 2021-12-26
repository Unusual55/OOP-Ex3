from api.GraphInterface import GraphInterface
from Objects.Edge import Edge
from Objects.Node import Node
from Objects.ReversedEdgesSet import ReversedEdgesSet
import copy

"""This class represent the directed weighted graph data structure, G=(V, E) where G is graph object, V is the
vertices, we implemented it as dictionary whrer the key of the node is the key, and it's value is the Node object
 that contain both it's key and it's 3 dimensional position. E is the Edges, we implemented it in two different
 stages:
 stage 1- the out edges. by definition, out edge is an edge e=(u,v ) the edge is strating from u and end in v, then
 we can say e is an out edge of u.
 we created a dictionary where the key is the key of the source node to another dictionary where the key is the
 key of the destenation node and the value is the Edge object.
 stage 2- the in edges. by definition, in edge is an edge e=(u, v) the edge is ending in v and starting from u, then
 we can say e is an in enge of v.
 we created a dictionary where the key is the key of the destenation node and the value is an ReversedEdgesSet,
 a custom set which we created in order to keep the keys of the source nodes who have out edges to the destenation
 node. As we said in the documentation of the ReversedEdgesSet class, we decided to implement it that way in order
 to reduce the time complexity of any search, add or remove from the set to O(1), to reduce the space complexity
 by keeping only the keys of the nodes instead of the edges, and of course prevent any case of duplicate edges in
 the graph"""


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes = dict()
        self.outEdges = dict()
        self.inEdges = {}
        self.nodecouter = 0
        self.edgecounter = 0
        self.mc = 0

    """This function counts and return how many nodes there are in the graph"""

    def v_size(self) -> int:
        return self.nodecouter

    """This function counts and return how many edges there are in the graph"""

    def e_size(self) -> int:
        return self.edgecounter

    """This function counts and return how many changes the graph has been through since the object created"""

    def get_mc(self) -> int:
        return self.mc

    """This function get 2 integer inputs which represent the keys of the source and destenation nodes and a float
    input which represent the weight of the edge. The function will add the edge to the graph if all of the following
    conditions has been met:
    1. Both nodes exist in the graph
    2. The weight is a non negative real number
    3. Both of the input keys are non negative integers
    4. The edge is not in the graph already"""

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodes.keys() or id2 not in self.nodes.keys() or id1 == id2 or weight <= 0 or id1 < 0 or id2 < 0:
            return False
        e = Edge(id1, id2, weight)
        if id1 in self.nodes.keys() and id2 in self.nodes.keys() and e in self.outEdges.get(id, {}).values():
            return False
        if id1 not in self.outEdges.keys():
            self.outEdges[id1] = {}
        if self.outEdges.get(id1, {}).get(id2) is not None and self.outEdges.get(id1, {}).get(id2) != e:  # TODO:CHECK
            self.edgecounter -= 1
        self.outEdges.get(id1, {})[id2] = e
        self.nodes.get(id1, Node).out_deg += 1
        self.nodes.get(id2, Node).in_deg += 1
        if self.inEdges.get(id2) is not None:
            self.inEdges[id2].add_edge(id1)
        else:
            self.inEdges[id2] = ReversedEdgesSet()
            self.inEdges[id2].add_edge(id1)
        self.mc += 1
        self.edgecounter += 1
        return True

    """This function get one integer input which represent the key of the new node and a tuple which represent the
    node's location in a 3 dimensional space. The function will create a new Node object and add it to the graph if
    and only if the following conditions has been met:
    1. All of the components in the coordination vector are valid floats
    2. The input key is a non negative integer
    3. There is no node with the same key in the graph"""

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        flag = True
        empty = False
        if pos is None:
            node = Node(node_id)
            empty = True
        elif pos[0] is None and pos[1] is None and pos[2] is None:
            node = Node(node_id)
            empty = True
        else:
            node = Node(node_id, pos[0], pos[1], pos[2])
        if node.checkpos():
            flag = True
        else:
            flag = True
            empty = True
        if flag:
            if empty:
                n = Node(node_id)
            else:
                n = Node(node_id, pos[0], pos[1], pos[2])
            if node_id in self.nodes or node_id < 0:
                return False
            self.nodes[node_id] = n
            self.nodecouter += 1
            self.mc += 1
            return True
        else:
            return False

    """This function get an integer input which represent a key of a node we would like to delete. The function will
    proceed to the delete process if and only if the input is a valid key of a node in the graph.
    Assuming the key is valid, The function will start by removing all of the occurences of the key as destenation
     node by using the set in inEdges while updating the number of edges in each iteration, then we will now remove
     all of the occurences of the key as source node, using the outEdges and remove them from inEdges while updating
     the edgecounter.
     The function will also remove any empty dictionary or set. After the function finished to remove the edges, it
     will update the mc and the nodecounter."""

    def remove_node(self, node_id: int) -> bool:
        removed = self.nodes.pop(node_id)
        if removed is not None:
            if removed.getKey() in self.inEdges.keys():
                for connectedNode in self.inEdges.get(node_id, ReversedEdgesSet):
                    self.outEdges.get(connectedNode, {}).pop(node_id)
                    self.nodes.get(connectedNode, Node).out_deg -= 1
                    self.edgecounter -= 1
                    if len(self.outEdges.get(connectedNode)) == 0:
                        self.outEdges.pop(connectedNode)
                self.inEdges.pop(node_id)
            if node_id in self.outEdges.keys():
                for e in self.outEdges.get(node_id, {}).values():
                    self.inEdges.get(e.get_dest(), ReversedEdgesSet).remove_edge(node_id)
                    self.nodes.get(e.get_dest(), Node).in_deg -= 1
                    self.edgecounter -= 1
                    if len(self.inEdges.get(e.get_dest(), ReversedEdgesSet)) == 0:
                        self.inEdges.pop(e.get_dest())
                self.outEdges.pop(node_id)
            self.nodecouter -= 1
            self.mc += 1
            return True
        return False

    """This function get two integer inputs which represents the keys of the source and destenation nodes we would
    like to delete the edge between them. The function will remove the edge if and only if the following conditions has
    been met:
    1. Both of the inputs are valid keys of nodes in the graph
    2. The source node's dictionary in outEdges is exist, which means it's not empty
    The function will remove the edge from outEdges and the key from the set in inEdges, it will update the
    edgecounter and the mc as well."""

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.nodes.keys() or node_id2 not in self.nodes.keys() or node_id1 not in self.outEdges.keys():
            return False
        removed = self.outEdges.get(node_id1, {}).pop(node_id2)
        if removed is not None:
            self.edgecounter -= 1
            self.mc += 1
            self.nodes.get(node_id1, Node).out_deg -= 1
        self.inEdges.get(node_id2, ReversedEdgesSet).remove_edge(node_id1)
        self.nodes.get(node_id2, Node).in_deg -= 1
        return True

    """This function return a dictionary which contain all of the nodes in the graph in the following format:
    dict[key] = Node, where key is the key of the node and Node is the Node object"""

    def get_all_v(self) -> dict:
        return self.nodes.copy()

    """This function get an integer input which represent the key of a node we would like to get a dictionary which
    contain it's in edges. The function use the keys in the ReversedEdgesSet to get the needed edges from outEdges
    and return a dictionary which contain the in edges by the following format:
    dict[key] = weight, where key is the key of the the destenation node and weight is the weight of the edge"""

    def all_in_edges_of_node(self, id1: int) -> dict:
        ret = {}
        if id1 not in self.nodes.keys() or id1 not in self.inEdges.keys():
            return ret

        for src in self.inEdges.get(id1, ReversedEdgesSet).get_keys():
            e = self.outEdges.get(src, {}).get(id1, Edge)
            ret[src] = e.get_weight()
        return ret

    """This function get one integer input which represent the key of a node we would like to get a dictionary which
     conatin all of the out edges that start from it, the function will return the internal dictionary in outEdges"""

    def all_out_edges_of_node(self, id1: int) -> dict:
        ret = {}
        if id1 in self.nodes.keys():
            for id2 in self.outEdges.get(id1, {}).keys():
                ret[id2] = self.outEdges.get(id1, {}).get(id2, Edge).get_weight()
        return ret

    def __eq__(self, other):
        if not isinstance(other, GraphInterface):
            return False
        mynodes = self.get_all_v()
        othernodes = other.get_all_v()
        if not mynodes.__eq__(othernodes):
            return False
        for node in mynodes.values():
            src = node.getKey()
            myinedges = self.all_in_edges_of_node(src)
            otherinedges = other.all_in_edges_of_node(src)
            if not myinedges.__eq__(otherinedges):
                return False
            myoutedges = self.all_out_edges_of_node(src)
            otheroutedges = self.all_out_edges_of_node(src)
            if not myoutedges.__eq__(otheroutedges):
                return False
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Graph: |V|=" + str(self.nodecouter) + ", |E|=" + str(self.edgecounter)

    def get_all_edges_time_saver(self):
        ret = dict()
        for key in self.nodes.keys():
            ret[key] = self.all_out_edges_of_node(key)
        return ret