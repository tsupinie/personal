
import os

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg

import numpy as np

import Tkinter as Tk
import tkFileDialog

import dorade

class SoloPyUI(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.pack()

        self._radar_data = 0

        self._figure = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self._figure.add_subplot(111, projection='polar')

        self._layout(self._figure)
        return

    def _layout(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        self._updateFigure()

#       toolbar = NavigationToolbar2TkAgg(canvas, self)
#       toolbar.update()
#       canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        quit_button = Tk.Button(master=self, text="Quit", command=self.quit)
        quit_button.pack(side=Tk.BOTTOM)

        self._buildMenu()
        return

    def _buildMenu(self):
        menu_bar = Tk.Menu(self)

        file_menu = Tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self._openFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.winfo_toplevel()['menu'] = menu_bar
        return
    
    def _openFile(self):

        options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Select a file to open'

        dorade_file_name = tkFileDialog.askopenfilename(**options)
        print "Opening %s ..." % dorade_file_name
        return

    def _updateFigure(self):
        sub = self._figure.axes[0]
        sub.gca()

        if type(self._radar_data) != int:
            sub.pcolormesh()
        return

def main():
    app = SoloPyUI()
    app.master.title("Tkinter Test")
    app.mainloop()
    return

if __name__ == "__main__":
    main()
