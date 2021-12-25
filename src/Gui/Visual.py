from typing import List
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.pyplot import Figure
from tkinter import simpledialog
from Objects.Node import Node
from Objects.DiGraph import DiGraph
from Objects.GraphAlgo import GraphAlgo


class Visual:
    # plt.tight_layout()
    counter = 0

    def __init__(self, g: DiGraph, fig: Figure):
        self.fig = fig
        self.g = g
        self.ax = fig.add_subplot(111)
        self.set_bbox()
        self.edgestack = []

        self.click = self.fig.canvas.mpl_connect('button_press_event', self.on_press)

        self.pick = self.fig.canvas.mpl_connect('pick_event', self.onpick)

        # self.ax.use_sticky_edges = False
        # self.ax.margins(tight=True)
        # self.ax.set_facecolor('dimgray')
        # self.ax.relim()
        # self.ax.autoscale()

    def on_press(self, event):

        print("mouse clicked: x: " + str(event.xdata) + " y: " + str(event.ydata) + "button: " + str(event.button))
        if event.button == MouseButton.RIGHT:
            key = self.add_node_by_click()
            self.add_node(key, (event.xdata, event.ydata, 0.0))

    def onpick(self, event):
        label = str(event.artist.get_label())
        if label.isalnum():
            key = int(label)
            if key not in self.g.get_all_v().keys():
                return
            if key in self.edgestack:
                self.remove_node(key)
                self.edgestack = []
                return
            self.edgestack.append(key)
            if len(self.edgestack) == 2:
                w = 0
                while True:
                    w = simpledialog.askfloat(title="Weight", prompt="Enter the weight of the edge")
                    if w <= 0:
                        continue
                    break
                self.add_edge(self.edgestack[0], self.edgestack[1], w)
                self.edgestack = []

    def set_bbox(self):
        minx, maxx, miny, maxy = float('inf'), float('-inf'), float('inf'), float('-inf')
        toupdate = []
        for key, node in self.g.get_all_v().items():
            if not node.checkpos():
                toupdate.append(key)
                continue
            minx = min(minx, node.get_x())
            maxx = max(maxx, node.get_x())
            miny = min(miny, node.get_y())
            maxy = max(maxy, node.get_y())
        self.xmin, self.xmax, self.ymin, self.ymax = minx, maxx, miny, maxy
        if minx == float('inf') and miny == float('inf') and maxx == float('-inf') and maxy == float('-inf'):
            self.xmin, self.ymin, self.xmax, self.ymax = -1.0, -1.0, 1.0, 1.0
        for do in toupdate:
            self.g.nodes.get(do, Node).setlimitedrandompos(self.xmin, self.ymin, 0.0, self.xmax, self.ymax, 0.0)

    def bbox_update(self, n: Node):
        if not n.checkpos():
            return
        self.xmin, self.xmax = min(self.xmin, n.get_x()), max(self.xmax, n.get_x())
        self.ymin, self.ymax = min(self.ymin, n.get_y()), max(self.ymax, n.get_y())

    def draw_graph(self):
        self.ax.clear()
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            self.ax.scatter(x1, y1, c='b', picker=5, label=str(src))
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='r', shrinkA=0, shrinkB=0))
        self.fig.canvas.draw()
        print(str(self.g.v_size()))

    def draw_graph_center(self):
        ga = GraphAlgo(self.g)
        key, dist = ga.centerPoint()
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src != key:
                self.ax.scatter(x1, y1, c='b', picker=5, label=str(src))
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='r', shrinkA=0, shrinkB=0))
        center = self.g.nodes.get(key, Node).getpos()
        self.ax.scatter(center[0], center[1], c='g', edgecolor='r')
        self.fig.canvas.draw()
        return key

    def draw_graph_SP(self, id1: int, id2: int):
        ga = GraphAlgo(self.g)
        dist, pathnodes = ga.shortest_path(id1, id2)
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src not in pathnodes:
                self.ax.scatter(x1, y1, c='b', picker=5, label=str(src))
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='r', shrinkA=0, shrinkB=0))
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
        self.fig.canvas.draw()
        return dist

    def draw_graph_TSP(self, cnodes: List[int]):
        ga = GraphAlgo(self.g)
        pathnodes, dist = ga.TSP(cnodes)
        for src, node in self.g.nodes.items():
            x1, y1 = node.get_x(), node.get_y()
            if src not in pathnodes:
                self.ax.scatter(x1, y1, c='b', picker=5, label=str(src))
            for dest in self.g.all_out_edges_of_node(src).keys():
                dnode = self.g.nodes.get(dest, Node)
                x2, y2 = dnode.get_x(), dnode.get_y()
                xy, xytext = [x1, y1], [x2, y2]
                self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                           facecolor='r', shrinkA=0, shrinkB=0))
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
        self.fig.canvas.draw()
        return dist

    def add_node(self, key: int, pos: tuple):
        if self.g.add_node(key, pos):
            self.ax.scatter(pos[0], pos[1], c='b', picker=5, label=str(key))
            self.fig.canvas.draw()

    def add_edge(self, src: int, dest: int, weight: float):
        if self.g.add_edge(src, dest, weight):
            snode = self.g.nodes.get(src, Node)
            dnode = self.g.nodes.get(dest, Node)
            x1, x2, y1, y2 = snode.get_x(), dnode.get_x(), snode.get_y(), dnode.get_y()
            xy, xytext = [x1, y1], [x2, y2]
            self.ax.annotate("", xy=xy, xytext=xytext, arrowprops=dict(arrowstyle="<|-", edgecolor='k',
                                                                       facecolor='r', shrinkA=0, shrinkB=0))
            self.fig.canvas.draw()

    def remove_node(self, key: int):
        if self.g.remove_node(key):
            self.draw_graph()

    def remove_edge(self, src: int, dest: int):
        if self.g.remove_edge(src, dest):
            self.draw_graph()

    def add_node_by_click(self):
        keys = self.g.get_all_v().keys()
        i = 0
        while i in keys:
            i += 1
        return i
