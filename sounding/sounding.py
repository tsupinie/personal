
import os
import urllib2
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
from matplotlib.transforms import Bbox, TransformedBbox

import numpy as np

import Tkinter as Tk
import tkFileDialog

from skewTlib import plotSounding, xyToTP, tpToXY
from parselib import parse
from dialoglib import SPCFileLoadDialog

class SoundingUI(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)

        self._figure = matplotlib.figure.Figure(figsize=(6, 8), dpi=95)

        self._p = []
        self._t = []
        self._td = []
        self._u = []
        self._v = []

        self._mouse_down = False
        self._dragging = None

        self._highlight_bg = None
        self._highlight = None

        self.grid()
        self._layout(self._figure)
        self.master.title("Sounding")

        self._updateCanvas()
        return

    def _layout(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1, column=1)

#       quit_button = Tk.Button(master=self, text="Quit", command=self.quit)
#       quit_button.grid(row=2, column=1)

        coord_frame = Tk.Frame(master=self) 

        p_label = Tk.Label(coord_frame, text="Pressure:")
        t_label = Tk.Label(coord_frame, text="Temperature:")
        self._p_coord = Tk.Label(coord_frame, text="-999.0 hPa", width=10)
        self._t_coord = Tk.Label(coord_frame, text="-999.0 C", width=10)

        p_label.grid(row=1, column=1)
        t_label.grid(row=2, column=1)
        self._p_coord.grid(row=1, column=2)
        self._t_coord.grid(row=2, column=2)

        coord_frame.grid(row=1, column=2)

        canvas.get_tk_widget().bind("<Motion>", self._mouseMove)
        canvas.get_tk_widget().bind("<Button-1>", self._mousePress)
        canvas.get_tk_widget().bind("<ButtonRelease-1>", self._mouseRelease)

        self._buildMenu()
        return

    def _buildMenu(self):
        menu_bar = Tk.Menu(self)

        file_menu = Tk.Menu(menu_bar, tearoff=0)

        file_open_menu = Tk.Menu(file_menu, tearoff=0)

        file_open_menu.add_command(label="From File", command=self._openFile)
        file_open_menu.add_command(label="From SPC", command=self._openSPC)

        file_menu.add_cascade(label="Open", menu=file_open_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.winfo_toplevel()['menu'] = menu_bar
        return

    def _updateCanvas(self):
        plotSounding(self._figure, p=self._p, t=self._t, td=self._td, u=self._u, v=self._v)

        if self._p == []:
            current_axes = self._figure.gca()
            self._sounding_bg = self._figure.canvas.copy_from_bbox(current_axes.bbox)

        self._highlight = None
        return

    def _openFile(self):

        options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Select a file to open'

        sounding_file_name = tkFileDialog.askopenfilename(**options)
        snd_data = parse(open(sounding_file_name, 'r'), 'pickle')

        if snd_data is not None:
            self._p = snd_data['pressure']
            self._t = snd_data['temperature']
            self._td = snd_data['dewpoint']
            self._u = snd_data['u_wind']
            self._v = snd_data['v_wind']

        self._updateCanvas()
        return

    def _openSPC(self):
        dialog = SPCFileLoadDialog(self)

        date = datetime.utcnow() - timedelta(hours=2)

        hour_to_mod = date.hour
        sounding_hour = int(hour_to_mod / 12) * 12
        date = date.replace(hour=sounding_hour, minute=0, second=0, microsecond=0)

        url = "http://www.spc.noaa.gov/exper/soundings/%s_OBS/%s.txt" % (date.strftime("%y%m%d%H"), dialog.result)
        snd_data = parse(urllib2.urlopen(url), 'spc')

        if snd_data is not None:
            self._p = snd_data['pressure']
            self._t = snd_data['temperature']
            self._td = snd_data['dewpoint']
            self._u = snd_data['u_wind']
            self._v = snd_data['v_wind']

        self._updateCanvas()
        return

    def _mouseMove(self, event):
#       self._updateCanvas()

        T, p = xyToTP(event.x, event.y, flip=True)[0]
        self._p_coord.config(text="%6.1f hPa" % p)
        self._t_coord.config(text="%6.1f C" % T)

        if self._p != [] and p >= self._p.min() and p <= self._p.max():
            circle_radius = 0.005
            current_axes = self._figure.gca()

            if self._dragging is None:
                idx = np.argmin(np.abs(p - self._p))
                line_dragging = None
            else:
                line_dragging, idx = self._dragging.split(':')
                idx = int(idx)

            if np.abs(T - self._t[idx]) < np.abs(T - self._td[idx]) or line_dragging == 't':
                highlight_pt = tpToXY(self._t[idx], self._p[idx])
                if self._mouse_down and self._dragging is None: 
                    self._dragging = "t:%d" % idx
                    line_dragging = 't'

                if self._mouse_down:
                    self._t[idx] = T
                    self._figure.canvas.restore_region(self._drag_bg)
                    self._figure.canvas.blit()
            else:
                highlight_pt = tpToXY(self._td[idx], self._p[idx])
                if self._mouse_down and self._dragging is None: 
                    self._dragging = "td:%d" % idx
                    dragging = 'td'

                if self._mouse_down:
                    self._td[idx] = T
                    self._figure.canvas.restore_region(self._drag_bg)
                    self._figure.canvas.blit()

            highlight_x, highlight_y = current_axes.transAxes.inverted().transform(highlight_pt)[0]

#           bbox_ctr_x, bbox_ctr_y = highlight_pt[0]
#           bbox_ur_x, bbox_ur_y = current_axes.transAxes.transform([[highlight_x + circle_radius, highlight_y + circle_radius]])[0]

#           bbox_half_size_x = bbox_ur_x - bbox_ctr_x
#           bbox_half_size_y = bbox_ur_y - bbox_ctr_y

#           bbox = Bbox([[bbox_ctr_x - bbox_half_size_x, bbox_ctr_y - bbox_half_size_y],[bbox_ctr_x + bbox_half_size_x, bbox_ctr_y + bbox_half_size_y]])
#           self._highlight_bg = self._figure.canvas.copy_from_bbox(bbox)

#           self._figure.canvas.restore_region(self._highlight_bg)

            if self._highlight is not None:
                current_axes.patches.remove(self._highlight)

            self._highlight = Circle((highlight_x, highlight_y), circle_radius, ec='k', fc='none', alpha=0.5, transform=current_axes.transAxes) 
            current_axes.add_patch(self._highlight)
 
            self._figure.canvas.draw()
            self._figure.canvas.blit()

        return

    def _mousePress(self, event):
        self._mouse_down = True

        if self._p != []:
            current_axes = self._figure.gca()

            T, p = xyToTP(event.x, event.y, flip=True)[0]
            idx = np.argmin(np.abs(p - self._p))

            dummy, y_upper_bound = current_axes.transAxes.inverted().transform(tpToXY(self._t[idx + 1], self._p[idx + 1], flip=False))[0]
            dummy, y_lower_bound = current_axes.transAxes.inverted().transform(tpToXY(self._t[idx - 1], self._p[idx - 1], flip=False))[0]

            drag_bbox_axes = Bbox([[0, y_lower_bound], [1, y_upper_bound]])
            drag_bbox = TransformedBbox(drag_bbox_axes, current_axes.transAxes)

            current_sounding = self._figure.canvas.copy_from_bbox(current_axes.bbox)
            self._figure.canvas.restore_region(self._sounding_bg)
            self._figure.canvas.blit(drag_bbox)

            self._drag_bg = self._figure.canvas.copy_from_bbox(drag_bbox)
#           self._figure.canvas.restore_region(current_sounding)
#           self._figure.canvas.blit(drag_bbox)

#           self._figure.canvas.restore_region(self._drag_bg)
        return

    def _mouseRelease(self, event):
        self._mouse_down = False
        self._dragging = None

        self._updateCanvas()
        return

def main():
    app = SoundingUI()
    app.mainloop()

if __name__ == "__main__":
    main()
