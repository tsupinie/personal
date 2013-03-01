
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import numpy as np

import Tkinter as Tk

class TkinterTest(Tk.Frame):
    def __init__(self, figure, master=None):
        Tk.Frame.__init__(self, master)
        self.pack()
        self._layout(figure)
        return

    def _layout(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        quit_button = Tk.Button(master=self, text="Quit", command=self.quit)
        quit_button.pack(side=Tk.BOTTOM)
        return

figure = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
sub = figure.add_subplot(111)
t = np.arange(-4.0, 4.1, 0.1)
s = t ** 2
sub.plot(t, s)

app = TkinterTest(figure)
app.master.title("Tkinter Test")
app.mainloop()
