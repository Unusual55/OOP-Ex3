from Objects.Edge import Edge
from Objects.Node import Node
from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph
import _heapq
from api.GraphInterface import GraphInterface
from api.GraphAlgoInterface import GraphAlgoInterface
import json
import pandas as pd
import numpy as np
import pathlib as path


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, *args):
        if len(args) == 0:
            self.g = DiGraph()
        else:
            self.g = DiGraph()
            for element in args:
                if isinstance(element, GraphInterface):
                    nodes = element.get_all_v()
                    for node in nodes.values():
                        self.g.add_node(node.getKey(), node.getpos())
                    for node in nodes.values():
                        inedges = element.all_in_edges_of_node(node.getKey())
                        for src in inedges.keys():
                            self.g.add_edge(src, node.getKey(), inedges.get(src))
                        outedges = element.all_out_edges_of_node(node.getKey())
                        for dest in outedges.values():
                            self.g.add_edge(node.getKey(), dest, outedges.get(dest))
                    return
                else:
                    continue

    def get_graph(self) -> GraphInterface:
        return self.g

    def plot_graph(self) -> None:
        vdict = self.g.get_all_v()
        min_x = float('inf')
        min_y = float('inf')
        min_z = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        max_z = float('-inf')
        keys = set()
        for node in vdict.values():
            if node.checkpos():
                min_x = min(min_x, node.get_x())
                max_x = max(max_x, node.get_x())
                min_y = min(min_y, node.get_y())
                max_y = max(max_y, node.get_y())
                min_z = min(min_z, node.get_z())
                max_z = max(max_z, node.get_z())
            else:
                keys.add(node.getKey())
        for i in keys:
            self.g.nodes.get(i, Node).setlimitedrandompos(minx=min_x, miny=min_y, minz=min_z, maxx=max_x, maxy=max_y,
                                                          maxz=max_z)

    def load_from_json(self, file_name: str) -> bool:
        pass

    """This function get a string input which represent the path for the new json file we would like to save.
    in case the path doesn't end with .json, which means it will be regular text file, the function will add the .json
    suffix to the path. The function will use the node dictionary function of DiGraph in order to get all of the nodes,
    and by using their keys we will also get their out edges.
    The function deal with regular and empty nodes in seperate ways, for regular nodes we will keep both id and position
    and for empty node we will keep only the id, by doing that the function can save both type of nodes to the same
    json file.
    Note: empty node is a node who doesn't have a position."""
    def save_to_json(self, file_name: str) -> bool:
        if not file_name.endswith(".json"):
            file_name += ".json"
        data = dict()
        nodes = list()
        ndict = self.g.get_all_v()
        edges = list()
        for node in ndict.values():
            if node.checkpos():
                pos = str(node.get_x()) + "," + str(node.get_y()) + "," + str(node.get_z())
                nodes.append({'id': node.getKey(), 'pos': pos})
            else:
                nodes.append({'id': node.getKey()})
            outlist = self.g.all_out_edges_of_node(node.getKey())
            for dest in outlist.keys():
                src = node.getKey()
                w = outlist.get(dest)
                edges.append({'src': src, 'w': w, 'dest': dest})
        data["Nodes"] = nodes
        data["Edges"] = edges
        with open(file_name, 'w') as fp:
            json.dump(data, fp, indent=4, )

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass
