from typing import List
# from Objects.Edge import Edge
from Objects.Node import Node
# from Objects.ReversedEdgesSet import ReversedEdgesSet
from Objects.DiGraph import DiGraph
from api.GraphInterface import GraphInterface
from api.GraphAlgoInterface import GraphAlgoInterface
import json
# import pandas as pd
# import numpy as np
from pathlib import Path
from collections import defaultdict
# from heapq import *
import heapq
from collections import defaultdict
from matplotlib.pyplot import Figure
import matplotlib.pyplot as plt


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

    """"The fucntion will return it's current graph"""

    def get_graph(self) -> GraphInterface:
        return self.g

    """Note: The graph might include few nodes who doesn't have a position, we can see that more easily in
    Node class and in the json files.
    This function calculates the 3d bounds of the graph, the minimal and maximal x, y, z values.
    After the calulations is finished, the function will look for any node in the graph who doesn't have a
    position, an empty node, and randomize x, y, z float values between the minimum and the maximal values."""

    def plot_graph(self) -> None:
        vdict = self.g.get_all_v()
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')
        min_z, max_z = float('inf'), float('-inf')
        keys = set()
        xlist, ylist = [], []
        for node in vdict.values():
            if node.checkpos():
                min_x, max_x = min(min_x, node.get_x()), max(max_x, node.get_x())
                xlist.append(node.get_x())
                min_y, max_y = min(min_y, node.get_y()), max(max_y, node.get_y())
                ylist.append(node.get_y())
                min_z, max_z = min(min_z, node.get_z()), max(max_z, node.get_z())
            else:
                keys.add(node.getKey())
        minfinity = min_x == float('inf') and min_y == float('inf') and min_z == float('inf')
        maxfinity = max_x == float('-inf') and max_y == float('-inf') and max_z == float('-inf')
        for i in keys:
            if not minfinity and not maxfinity:
                self.g.nodes.get(i, Node).setlimitedrandompos(minx=min_x, miny=min_y, minz=min_z,
                                                              maxx=max_x, maxy=max_y, maxz=max_z)
                node = self.g.nodes.get(i, Node)
                xlist.append(node.get_x())
                ylist.append(node.get_y())
            else:
                min_x, min_y, min_z = 0, 0, 0
                max_x, max_y, max_z = 10, 10, 10
                self.g.nodes.get(i, Node).setlimitedrandompos(minx=min_x, miny=min_y, minz=min_z,
                                                              maxx=max_x, maxy=max_y, maxz=max_z)
                node = self.g.nodes.get(i, Node)
                xlist.append(node.get_x())
                ylist.append(node.get_y())
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(xlist, ylist, c='b')
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            ax.scatter(x1, y1, c='b', picker=5, label=str(src))
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='r', shrinkA=0, shrinkB=0))
        plt.show()


    """This function get a string input which represent the path to the json file we would like to load.
    The function will check if the path is valid and the file indeed exist, if it's not, the function won't
    do anything.
    Assuming the path is valid, the function will create a new graph, deserialize the nodes and edges and add
    them to the graph. In any case the json contain invalid inputs, the function will raise an exception,
    return false and won't set the graph as the current graph. Assuming the input is valid, the function will
    set the graph as the new graph"""

    def load_from_json(self, file_name: str) -> bool:
        if not Path.exists(Path(file_name)):
            return False
        f = open(file_name)
        data = json.load(f)
        nodedata = data.get("Nodes")
        edgedata = data.get("Edges")
        loadgraph = DiGraph()
        for n in nodedata:
            if len(n) == 1:
                loadgraph.add_node(n.get("id"), (None, None, None))
            elif len(n) == 2:
                key = n.get("id")
                postr = str(n.get("pos"))
                splitted = postr.split(',')
                x = float(splitted[0])
                y = float(splitted[1])
                z = float(splitted[2])
                loadgraph.add_node(key, (x, y, z))
        for e in edgedata:
            src = e.get("src")
            w = e.get("w")
            dest = e.get("dest")
            loadgraph.add_edge(src, dest, w)
        self.g = loadgraph
        f.close()
        return True

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

    """The function get two function which represent two vertices in the graph which we would like to
    calculate and return the shortest distance and the shortest path between them.
    Using Dijkstra algorithm which we implemented using Priority Queue we get two dictionaries, the first
    contains the distance to any other vertex in the graph and the second contain the previous node of every 
    node. Using support function and the second dictionary we can restore the path.
    Time Complexity: O(|E|+|V|log|V|+|V|)~ O(|E|+|V|log|V|) where E is the number of edges in the graph and 
    V is the number of nodes"""

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if id1 not in self.g.get_all_v() or id2 not in self.g.get_all_v() or id1 == id2:
            return -1, []
        dijkstra_output = self.dijkstra(id1)
        if dijkstra_output == (float('inf'), []):
            return dijkstra_output
        prevs = dijkstra_output[1]
        dists = dijkstra_output[0]
        if id2 not in dists:
            return float('inf'), []
        distance = dists.get(id2)
        path = []
        path = self.dijkstra_path(prevs, id1, id2)
        return distance, path

    """This function is our implementation for Dijkstra algorithm using Priority Queue-> Binary Heap
    We decided to use defaultdict, which is a special type of dictionary that return a default value in any
    case a wanted key is not in the dictionary.
    Time Complexity: O(|E|+|V|log|V|) where E is the number of edges in the graph and V is the number of nodes"""

    def dijkstra(self, src: int):
        distance = defaultdict(lambda: float('inf'))
        prev = dict()
        visited = set()
        pq = []
        distance[src] = 0
        heapq.heappush(pq, (0, src))
        if len(self.g.all_out_edges_of_node(src)) == 0:
            return float('inf'), []
        while pq:
            s = heapq.heappop(pq)
            node, dist = s[1], s[0]
            visited.add(node)
            for neighbor, weight in self.g.all_out_edges_of_node(node).items():
                if neighbor in visited:
                    continue
                newdist = dist + weight
                if distance[neighbor] > newdist:
                    prev[neighbor] = node
                    distance[neighbor] = newdist
                    heapq.heappush(pq, (newdist, neighbor))
        return distance, prev

    """This function is another implementation of Dijkstra algorithm, the only difference is that it returns
    only the distance dictionary.
    Time Complexity: O(|E|+|V|log|V|) where E is the number of edges in the graph and V is the number of nodes"""

    def dijkstra_distance(self, src: int):
        distance = defaultdict(lambda: float('inf'))
        visited = set()
        pq = []
        distance[src] = 0
        heapq.heappush(pq, (0, src))
        if len(self.g.all_out_edges_of_node(src)) == 0:
            return float('inf'), []
        while pq:
            s = heapq.heappop(pq)
            node, dist = s[1], s[0]
            visited.add(node)
            for neighbor, weight in self.g.all_out_edges_of_node(node).items():
                if neighbor in visited:
                    continue
                newdist = dist + weight
                if distance[neighbor] > newdist:
                    distance[neighbor] = newdist
                    heapq.heappush(pq, (newdist, neighbor))
        return distance

    """This function get two integer inputs which represent the source and the destenation vertices which
    we would like to restore between them and one dictionary which contains the previous node of every key,
    node: previous[node].
    The function restore the shortest path from destenation vertex back to the source vertex using the
    previous dictionary
    Time Complexity: O(V) where V is the number of vertices in the graph"""

    def dijkstra_path(self, nodes: dict, src: int, dest: int) -> list:
        ret = list()
        index = dest
        ret.append(dest)
        while index != src:
            index = nodes.get(index)
            ret.insert(0, index)
        return ret

    """Max shortest path: The longest path among all of the shortest paths of vertex v. ->M_i, where i is the
    index of the node
    Let M be a set of Max shortest paths of every vertex in the graph. Assuming k is the key of the center
    node, then foreach m in M M_k<m. In this case we can say that k is the center node, since it's max
    shortest path is the minimal among all of the vertices in the graph.
    The function using dijkstra algorithm calculate all of the shortest path to all of the vertices and check
    which node has the minimal max shortest path.
    Time Complexity: O(|V|*(|E| +|V|log|V|)) where V is the number of vertices and E is the number of edges
    """

    def centerPoint(self) -> (int, float):
        nodes = self.g.get_all_v()
        minid = -1
        mindist = float('inf')
        for key in nodes.keys():
            if minid == -1:
                minid = key
            dist = self.dijkstra_distance(key)
            if len(dist) == 2:
                return
            vmax = float('-inf')
            for d in dist.values():
                vmax = max(d, vmax)
            if vmax < mindist:
                minid = key
                mindist = vmax
        return minid, mindist

    """Note: data: Tuple which contain a dictionary of distance and a dictionary of previous nodes
             dijkstree: A dictionary of data.
    This function get a list of nodes which represent vertices we have to visit.
    This implementation have 3 parts:
    1. Setup dijkstree for each node:
    The function will run dijkstra on a node from the list, and get data as output.
    The function will use TSP_space_saver function who will remove any unnecessary values from the distance
    dictionary in data in order to reduce the space complexity.
    The function will add data to dijkstree where the key is the key of the node and data is the value
    2. Greedy TSP for each node:
    The function will loop through the list of nodes.
    for each node the function will call a support function easy_tsp_v3 who will calculate a path and distance
    that start from the node using greedy approach. Since we already calculate the distances and paths, we can
    use them to calculate the path and the distance.
    3. Compare and Keep:
    Each iteration we will get a the path and the distance from easy_tsp_v3, The function will check if the
    distance we got is smaller than the one we already have, and if it is, we will set it as the minimal, and
    set the path as the best path.
    Time Complexity: O(k^2(|E|+|V|log|V|)+k^3)"""

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        dijkstree = dict()
        for i in node_lst:
            data = self.dijkstra(i)
            data = self.TSP_space_saver(i, set(node_lst), data)
            """In case one or more of the nodes is not in the same strongly connected component"""
            if data.__eq__((-1, [])):
                return data
            dijkstree[i] = data
        best_path = []
        mindist = float('inf')
        for key in node_lst:
            tsp_out = self.easy_tsp_v3(key, set(node_lst), dijkstree)
            curr_path = tsp_out[0]
            curr_dist = tsp_out[1]
            if curr_dist < mindist:
                mindist = curr_dist
                best_path = curr_path
        return best_path, mindist

    """This function is a support function for TSP, it's only purpose is to remove any key who doesn't appear
    in the list of nodes from the data. This function reduce the space complexity of the whole dijkstree.
    Time Complexity: O(k) where k is the size of the node list"""

    def TSP_space_saver(self, key: int, node_set: set[int], data: dict):
        distance = data[0]
        path = data[1]
        newdistance = dict()
        for i in node_set:
            if i not in distance.keys():
                return -1, []
            newdistance[i] = distance.get(i)
        distance = newdistance
        return distance, path

    """This function calculates the optimal path using greedy approach-> each time the next node will be the
    closest one which we didn't visit yet. The function get one integer input which represent the node we will
    start from, a set of integers which represent the set of nodes we need to visit and of course dijkstree.
    The function will define it's current path and distance dictionaries from dijkstree, then the function
    will calculate the next node using greedy approach. At the end of every while iteration the function will
    add the current node to the path and set the next one, increase the minimal distance by the distance of
    the path from current node to the next node and redefine the distance and path dictionary from dijkstree
    so it will suit the next iteration current node
    Time Complexity: O(k^2), where k is the size of the node set"""
    #TODO: use profiler to improve performance
    def easy_tsp_v3(self, src: int, node_set: set[int], dijkstree: dict):
        curr, currdist = src, 0
        distance, path = dijkstree.get(curr, ())
        visited = set()
        tsp_path = []
        while len(visited) != len(node_set) - 1:
            visited.add(curr)
            nextid = -1
            currmindist = float('inf')
            for nextnode in node_set:
                if nextnode == curr or nextnode in visited:
                    continue
                if nextid == -1:
                    nextid = nextid
                if distance.get(nextnode) < currmindist:
                    nextid = nextnode
                    currmindist = distance.get(nextnode)
            tspath = self.dijkstra_path(path, curr, nextid)
            if len(tsp_path) > 0 and tspath[0] == tsp_path[-1]:
                tspath.pop(0)
            tsp_path.extend(tspath)
            curr = nextid
            currdist += currmindist
            distance = dijkstree.get(curr, ())[0]
            path = dijkstree.get(curr, ())[1]
        return tsp_path, currdist

    """Section of thrown TSP version- the one we handed in is TSP_v3"""
    # def TSP_v2(self, node_lst: List[int]) -> (List[int], float):
    #     if len(node_lst) == 1:
    #         return node_lst, 0
    #     minid = -1
    #     mindist = float('inf')
    #     bestpath = []
    #     for i in node_lst:
    #         if minid == -1:
    #             minid = i
    #         result = self.single_source_tsp(node_lst.copy(), i)
    #         dist = result[1]
    #         path = result[0]
    #         if result[1] == -1:
    #             return node_lst, -1
    #         if dist < mindist:
    #             mindist = dist
    #             minid = i
    #             bestpath = path
    #     return bestpath, mindist
    #
    # def single_source_tsp(self, node_lst: List[int], src: int):
    #     if len(node_lst) == 1:
    #         return node_lst, 0
    #     currnode = node_lst[src]  # change to constant after threading single source tsp
    #     path = []
    #     finaldist = 0
    #     unvisitedcities = set()
    #     for i in node_lst:
    #         unvisitedcities.add(i)
    #     while len(unvisitedcities) > 0:
    #         dijkstra_output = self.Dijkstra(currnode)
    #         distance = dijkstra_output[0]
    #         paths = dijkstra_output[1]
    #         nextnode = -1
    #         mindist = float('inf')
    #         for v in unvisitedcities:
    #             if v == currnode:
    #                 continue
    #             if distance.get(v) == 'inf':
    #                 return node_lst, -1  # if the list is not in the same connection component-> check what to do!!!
    #             if nextnode == -1:
    #                 nextnode = v
    #             if distance.get(v) < mindist:
    #                 mindist = distance.get(v)
    #                 nextnode = v
    #         path.insert(0, currnode)
    #         finaldist += mindist
    #         unvisitedcities.remove(currnode)
    #         currnode = nextnode
    #     return path, finaldist
    #
    # def TSP_v1(self, node_lst: List[int]) -> (List[int], float):
    #     if len(node_lst) == 1:
    #         return node_lst, 0
    #     currnode = node_lst[0]  # change to constant after threading single source tsp
    #     path = []
    #     finaldist = 0
    #     unvisitedcities = set()
    #     for i in node_lst:
    #         unvisitedcities.add(i)
    #     while len(unvisitedcities) > 0:
    #         dijkstra_output = self.Dijkstra(currnode)
    #         distance = dijkstra_output[0]
    #         paths = dijkstra_output[1]
    #         nextnode = -1
    #         mindist = float('inf')
    #         for v in unvisitedcities:
    #             if v == currnode:
    #                 continue
    #             if distance.get(v) == 'inf':
    #                 return node_lst, -1  # if the list is not in the same connection component-> check what to do!!!
    #             if nextnode == -1:
    #                 nextnode = v
    #             if distance.get(v) < mindist:
    #                 mindist = distance.get(v)
    #                 nextnode = v
    #         path.insert(0, currnode)
    #         finaldist += mindist
    #         unvisitedcities.remove(currnode)
    #         currnode = nextnode
    #     return path, finaldist
    #
    # def dijkstra_path_dyprog(self, src: int, dest: int, distance: dict):
    #     ret = []
    #     curr = self.g.nodes.get(dest, Node)
    #     index = dest
    #     while index != src:
    #         ret.insert(0, index)
    #         inedges = self.g.all_in_edges_of_node(index).items()
    #         for prev, weight in inedges:
    #             if distance.get(prev) == distance.get(index) - weight:
    #                 index = prev
    #                 break
    #     return ret
    # def Dijkstra(self, src: int):
    #     visited = dict()
    #     distance = dict()
    #     nodes = dict()
    #     prev = dict()
    #     for i in self.g.get_all_v().keys():
    #         visited[i] = False
    #         if src == i:
    #             distance[i] = 0
    #             prev[i] = i
    #         else:
    #             distance[i] = float('inf')
    #             prev[i] = None
    #         nodes[i] = None
    #     heap = FibonacciHeap()
    #     for i in self.g.get_all_v().keys():
    #         nodes[i] = heap.insert(float('inf'), i)
    #     heap.decrease_key(nodes.get(src), 0)
    #     while heap.total_nodes:
    #         curr = heap.extract_min()
    #         # currkey = curr.key
    #         currkey = curr.value
    #         visited[currkey] = True
    #         if curr is None:
    #             break
    #         for neighbor in self.g.all_out_edges_of_node(currkey).keys():
    #             if not visited.get(neighbor):
    #                 dist = self.g.outEdges.get(currkey, {}).get(neighbor, Edge).get_weight()
    #                 if distance.get(currkey) + dist < distance.get(neighbor):
    #                     distance[neighbor] = dist + distance.get(currkey)
    #                     prev[neighbor] = currkey
    #                     heap.decrease_key(nodes[neighbor], distance[neighbor])
    #     return distance, prev
# def Dijkstra_distance(self, src: int):
#     visited = dict()
#     distance = dict()
#     nodes = dict()
#     for i in self.g.get_all_v().keys():
#         visited[i] = False
#         if src == i:
#             distance[i] = 0
#         else:
#             distance[i] = float('inf')
#         nodes[i] = None
#     heap = FibonacciHeap()
#     for i in self.g.get_all_v().keys():
#         nodes[i] = heap.insert(float('inf'), i)
#     heap.decrease_key(nodes.get(src), 0)
#     while heap.total_nodes:
#         curr = heap.extract_min()
#         currkey = curr.value
#         visited[currkey] = True
#         if curr is None:
#             break
#         for neighbor in self.g.all_out_edges_of_node(currkey).keys():
#             if not visited.get(neighbor):
#                 dist = self.g.outEdges.get(currkey, {}).get(neighbor, Edge).get_weight()
#                 if distance.get(currkey) + dist < distance.get(neighbor):
#                     distance[neighbor] = dist + distance.get(currkey)
#                     heap.decrease_key(nodes[neighbor], distance[neighbor])
#     return distance

# def Dijkstra_distance_path(self, src: int, dest: int):
#     visited = dict()
#     distance = dict()
#     nodes = dict()
#     prev = dict()
#     for i in self.g.get_all_v().keys():
#         visited[i] = False
#         if src == i:
#             distance[i] = 0
#             prev[i] = i
#         else:
#             distance[i] = float('inf')
#             prev[i] = None
#         nodes[i] = None
#     heap = FibonacciHeap()
#     for i in self.g.get_all_v().keys():
#         nodes[i] = heap.insert(float('inf'), i)
#     heap.decrease_key(nodes.get(src), 0)
#     while heap.total_nodes:
#         curr = heap.extract_min()
#         # currkey = curr.key
#         currkey = curr.value
#         visited[currkey] = True
#         if curr is None:
#             break
#         for neighbor in self.g.all_out_edges_of_node(currkey).keys():
#             if not visited.get(neighbor):
#                 dist = self.g.outEdges.get(currkey, {}).get(neighbor, Edge).get_weight()
#                 if distance.get(currkey) + dist < distance.get(neighbor):
#                     distance[neighbor] = dist + distance.get(currkey)
#                     prev[neighbor] = currkey
#                     heap.decrease_key(nodes[neighbor], distance[neighbor])
#     return distance.get(dest), prev
