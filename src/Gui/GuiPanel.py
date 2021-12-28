import sys
import os

sys.path.insert(0, os.path.abspath(__file__).rsplit(os.sep, 2)[0])

import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk as ttk
from matplotlib.pyplot import Figure

import matplotlib

from Gui.PMenuBar import PMenuBar

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
from Visual import Visual
from Objects.DiGraph import DiGraph

style.use("ggplot")

""" This class represents the GUI panel, in this class we embedded the matplotlib into tkinter."""


class GuiPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.f = Figure()
        self.vision = Visual(DiGraph(), self.f)
        menubar = PMenuBar(self.vision, self, self.f)
        parent.config(menu=menubar)

        self.canvas = FigureCanvasTkAgg(self.f, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)


root = tk.Tk()
GuiPanel(root)
root.mainloop()
