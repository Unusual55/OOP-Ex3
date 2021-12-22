from typing import List
import matplotlib
import matplotlib.pyplot as plt
from Objects.Node import Node
from Objects.DiGraph import DiGraph
from Objects.GraphAlgo import GraphAlgo


class Visual:
    fig = plt.figure()
    plt.tight_layout()
    ax = plt.subplot()
    ax.use_sticky_edges = False
    ax.margins(tight=True)
    ax.set_facecolor('dimgray')
    ax.relim()
    ax.autoscale()
    tm = fig.canvas.manager.toolmanager

    def __init__(self, g: DiGraph):
        self.g = g

    def set_bbox(self):
        minx, maxx, miny, maxy = float('inf'), float('-inf'), float('inf'), float('-inf')
        for node in self.g.get_all_v():
            if not node.checkpos():
                continue
            minx = min(minx, node.get_x())
            maxx = max(maxx, node.get_x())
            miny = min(miny, node.get_y())
            maxy = max(maxy, node.get_y())
        self.xmin, self.xmax, self.ymin, self.ymax = minx, maxx, miny, maxy

    def bbox_update(self, n: Node):
        if not n.checkpos():
            return
        self.xmin, self.xmax = min(self.xmin, n.get_x()), max(self.xmax, n.get_x())
        self.ymin, self.ymax = min(self.ymin, n.get_y()), max(self.ymax, n.get_y())

    def draw_graph(self):
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            self.ax.scatter(x1, y1, c='b')
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='k', shrinkA=0, shrinkB=0))
        plt.show()

    def draw_graph_center(self):
        ga = GraphAlgo(self.g)
        key, dist = ga.centerPoint()
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src != key:
                self.ax.scatter(x1, y1, c='b')
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='k', shrinkA=0, shrinkB=0))
        center = self.g.nodes.get(key, Node).getpos()
        self.ax.scatter(center[0], center[1], c='g', edgecolor='r')
        plt.show()

    def draw_graph_SP(self, id1: int, id2: int):
        ga = GraphAlgo(self.g)
        dist, pathnodes = ga.shortest_path(id1, id2)
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src not in pathnodes:
                self.ax.scatter(x1, y1, c='b')
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='k', shrinkA=0, shrinkB=0))
        prev = pathnodes.pop(0)
        src = self.g.nodes.get(prev, Node)
        self.ax.scatter(src.get_x(), src.get_y(), c='yellow')
        for n in pathnodes:
            dest = self.g.nodes.get(n, Node)
            self.ax.scatter(dest.get_x(), dest.get_y(), c='yellow')
            xy, xytext = [src.get_x(), src.get_y()], [dest.get_x(), dest.get_y()]
            self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='darkorange',
                                                                       facecolor='darkorange', shrinkA=0, shrinkB=0),
                             annotation_clip=True)
            src = dest
        plt.show()

    def draw_graph_TSP(self, cnodes: List[int]):
        ga = GraphAlgo(self.g)
        pathnodes, dist = ga.TSP(cnodes)
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src not in pathnodes:
                self.ax.scatter(x1, y1, c='b')
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='k', shrinkA=0, shrinkB=0))
        prev = pathnodes.pop(0)
        src = self.g.nodes.get(prev, Node)
        self.ax.scatter(src.get_x(), src.get_y(), c='hotpink')
        for n in pathnodes:
            dest = self.g.nodes.get(n, Node)
            self.ax.scatter(dest.get_x(), dest.get_y(), c='hotpink')
            xy, xytext = [src.get_x(), src.get_y()], [dest.get_x(), dest.get_y()]
            self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='lime',
                                                                       facecolor='lime', shrinkA=0, shrinkB=0),
                             annotation_clip=None)
            src = dest
        plt.show()

    def add_node(self, key: int, pos: tuple):
        if self.g.add_node(key, pos):
            self.ax.scatter(pos[0], pos[1], c='b')
            plt.show()

    def add_edge(self, src: int, dest: int, weight: float):
        if self.add_edge(src, dest, weight):
            snode = self.g.nodes.get(src, Node)
            dnode = self.g.nodes.get(dest, Node)
            x1, x2, y1, y2 = snode.get_x(), dnode.get_x(), snode.get_y(), dnode.get_y()
            xy, xytext = [x1, y1], [x2, y2]
            self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                       facecolor='k', shrinkA=0, shrinkB=0))
            plt.show()

    def remove_node(self, key: int):
        if self.g.remove_node(key):
            self.draw_graph()

    def remove_node(self, key: int):
        if self.g.remove_node(key):
            self.draw_graph()
