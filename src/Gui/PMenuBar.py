import tkinter as tk
from tkinter import ttk as ttk

from matplotlib.figure import Figure

from Visual import Visual
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Objects.GraphAlgo import GraphAlgo


class PMenuBar(tk.Menu):
    def __init__(self, vision: Visual, ws, f: Figure):
        tk.Menu.__init__(self, ws)
        self.vision = vision
        self.f = f

        file = tk.Menu(self, tearoff=False)
        file.add_command(label="New Graph")
        file.add_command(label="Load Graph", command=self.load_graph)
        file.add_command(label="Save Graph", command=self.save_graph)

        edit = tk.Menu(self, tearoff=False)
        edit.add_command(label="Add Node")
        edit.add_command(label="Add Edge")
        edit.add_command(label="Remove Node")
        edit.add_command(label="Remove Edge")

        algo = tk.Menu(self, tearoff=False)
        algo.add_command(label="Center Point")
        algo.add_command(label="Shortest Path")
        algo.add_command(label="TSP")

        self.add_cascade(label="File", menu=file)
        self.add_cascade(label="Edit Graph", menu=edit)
        self.add_cascade(label="Algorithms", menu=algo)

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


