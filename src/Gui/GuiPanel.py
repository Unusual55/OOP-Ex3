import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk as ttk

import matplotlib

from Gui.PMenuBar import PMenuBar

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from Visual import Visual
from Objects.DiGraph import DiGraph

style.use("ggplot")


class GuiPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # label = tk.Label(self, text="Graph!")
        # label.pack(pady=10, padx=10, side=tkinter.TOP, fill=tkinter.BOTH)
        self.f = Figure()
        # a = self.f.add_subplot(111)
        self.vision = Visual(DiGraph(), self.f)
        menubar = PMenuBar(self.vision, self, self.f)
        canvas = FigureCanvasTkAgg(self.f, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        parent.config(menu=menubar)

GuiPanel(tk.Tk())