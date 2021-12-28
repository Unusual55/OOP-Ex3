import sys
import os
sys.path.insert(0, os.path.abspath(__file__).rsplit(os.sep, 2)[0])
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import simpledialog

from matplotlib.pyplot import Figure

from Objects.DiGraph import DiGraph
from Visual import Visual
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Objects.GraphAlgo import GraphAlgo


""" This class represents the controller behind the menubar in out GUI. In this class we create the menubar, add its sub-menus and menum items, and of course trigger the 
events which control the visual graph."""

class PMenuBar(tk.Menu):
    def __init__(self, vision: Visual, ws, f: Figure):
        tk.Menu.__init__(self, ws)
        self.vision = vision
        self.f = f
        self.ws = ws
        file = tk.Menu(self, tearoff=False)
        file.add_command(label="New Graph", command=self.new_graph)
        file.add_command(label="Load Graph", command=self.load_graph)
        file.add_command(label="Save Graph", command=self.save_graph)

        edit = tk.Menu(self, tearoff=False)
        edit.add_command(label="Add Node", command=self.add_node)
        edit.add_command(label="Add Edge", command=self.add_edge)
        edit.add_command(label="Remove Node", command=self.remove_node)
        edit.add_command(label="Remove Edge", command=self.remove_edge)

        algo = tk.Menu(self, tearoff=False)
        algo.add_command(label="Center Point", command=self.center)
        algo.add_command(label="Shortest Path", command=self.sp_data)
        algo.add_command(label="TSP", command=self.tsp_data)

        self.add_cascade(label="File", menu=file)
        self.add_cascade(label="Edit Graph", menu=edit)
        self.add_cascade(label="Algorithms", menu=algo)

    """ This function allow us to use file chooser in order to load a json file into graph. """    
        
    def load_graph(self):
        ga = GraphAlgo()
        path = askopenfilename()
        try:
            ga.load_from_json(path)
            g = ga.get_graph()
            self.f.clear()
            self.vision = Visual(g, self.f)
            self.vision.draw_graph()
        except:
            popup = tk.Tk()
            popup.geometry('100x100')
            popup.winfo_toplevel()
            popup.wm_title("Error")
            label = ttk.Label(popup, text="Something went wrong")
            label.pack(side="top", fill="x", pady=10)
            b1 = ttk.Button(popup, text="OK", command=popup.destroy)
            b1.pack()
            popup.mainloop()

     """ This function allow us to save our graph into .json file using a file saver and of course out save_to_json function """
            
    def save_graph(self):
        g = self.vision.g
        ga = GraphAlgo(g)
        path = asksaveasfilename()
        ga.save_to_json(path)
        try:
            popup = tk.Tk()
            popup.geometry('100x100')
            popup.winfo_toplevel()
            popup.wm_title("Save")
            label = ttk.Label(popup, text="The graph saved successfully!")
            label.pack(side="top", fill="x", pady=10)
            b1 = ttk.Button(popup, text="OK", command=popup.destroy)
            b1.pack()
            popup.mainloop()
        except:
            popup = tk.Tk()
            popup.geometry('100x100')
            popup.winfo_toplevel()
            popup.wm_title("Error")
            label = ttk.Label(popup, text="Something went wrong")
            label.pack(side="top", fill="x", pady=10)
            b1 = ttk.Button(popup, text="OK", command=popup.destroy)
            b1.pack()
            popup.mainloop()

    """ This function resets the graph """
            
    def new_graph(self):
        self.vision.g = DiGraph()
        self.vision.ax.clear()
        self.vision.draw_graph()

    """ This function will trigger center algorithm on the grpah """
        
    def center(self):
        key = self.vision.draw_graph_center()
        popup = tk.Tk()
        popup.geometry('100x100')
        popup.winfo_toplevel()
        popup.wm_title("Save")
        label = ttk.Label(popup, text="The center node is" + str(key))
        label.pack(side="top", fill="x", pady=10)
        b1 = ttk.Button(popup, text="OK", command=popup.destroy)
        b1.pack()
        popup.mainloop()

    """ This function will trigger an add node user input """
        
    def add_node(self):
        key = simpledialog.askinteger(title="Id Entry", prompt="Enter the key of the node", )
        if key < 0 or key in self.vision.g.nodes.keys():
            simpledialog.messagebox.showerror(title="Error", message="The key can't be negative and"
                                                                     "cant exist in the graph already")
            return
        x = simpledialog.askfloat("X Entry", prompt="Enter the X value")
        y = simpledialog.askfloat("Y Entry", prompt="Enter the Y value")
        z = simpledialog.askfloat("Z Entry", prompt="Enter the Z value")
        self.vision.add_node(key, (x, y, z))

    """ This function will trigger an add edge use input """
        
    def add_edge(self):
        src = simpledialog.askinteger(title="Source Entry", prompt="Enter the source id")
        if src not in self.vision.g.nodes.keys():
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist")
            return
        dest = simpledialog.askinteger(title="Destenation Entry", prompt="Enter the destenation id")
        if dest in self.vision.g.nodes.keys() and self.vision.g.outEdges.get(src, {}).get(dest) is not None:
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist or"
                                                                     " The edge already exists")
            return
        w = simpledialog.askfloat(title="Weight Entry", prompt="Enter the weight of the edge")
        if w <= 0:
            simpledialog.messagebox.showerror(title="Error", message="The weight have to be positive number")
            return
        self.vision.add_edge(src, dest, w)

    """ This function will trigger remove node user input"""
        
    def remove_node(self):
        key = simpledialog.askinteger(title="Id Entry", prompt="Enter the id of the node you would like"
                                                               " to remove")
        if key in self.vision.g.nodes.keys():
            self.vision.remove_node(key)

    """ This function will trigger remove edge user input"""
            
    def remove_edge(self):
        src = simpledialog.askinteger(title="Source Entry", prompt="Enter the source id")
        if src not in self.vision.g.nodes.keys():
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist")
            return
        dest = simpledialog.askinteger(title="Destenation Entry", prompt="Enter the destenation id")
        if dest in self.vision.g.nodes.keys() and self.vision.g.outEdges.get(src, {}).get(dest) is not None:
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist or"
                                                                     " The edge already exists")
            return
        self.vision.remove_edge(src, dest)

    def draw(self):
        self.f.clear()
        self.canvas.draw_idle()

    """ This function will trigger shortest path user input and then run the algorithms on the graph"""
        
    def sp_data(self):
        src = simpledialog.askinteger(title="Source Entry", prompt="Enter the source id")
        if src not in self.vision.g.nodes.keys():
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist")
            return
        dest = simpledialog.askinteger(title="Destenation Entry", prompt="Enter the destenation id")
        if dest not in self.vision.g.nodes.keys():
            simpledialog.messagebox.showerror(title="Error", message="The key you entered doesn't exist or"
                                                                     " The edge already exists")
            return
        dist = self.vision.draw_graph_SP(src, dest)
        simpledialog.messagebox.showinfo(title="Result", message="The shortest distance between " + src + " and "
                                         + dest + " is " + dist)

    """ This function will trigger shortest path user input and then run the algorithms on the graph"""
        
    def tsp_data(self):
        nodes = set()
        node_lst = []
        key = 0
        while key >= 0:
            key = simpledialog.askinteger(title="Node id entry", prompt="Enter any node id or negative number to end this")
            if key < 0:
                break
            if key in nodes:
                continue
            nodes.add(key)
            node_lst.append(key)
        dist = self.vision.draw_graph_TSP(node_lst)
        simpledialog.messagebox.showinfo(title="Result", message="The distance of the path is " + dist)
