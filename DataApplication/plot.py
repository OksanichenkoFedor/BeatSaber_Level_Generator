import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import FuncFiles.config as config
from scipy.fft import fft, fftfreq
import numpy as np

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure


class PlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=config.figsize, dpi=100, tight_layout=True)
        self.a = self.f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def replot(self):
        self.a.clear()
        self.a.grid()
        data = self.master.logger.get_plot_time()
        self.a.plot(data[0], label="Download time")
        self.a.plot(data[1], label="Converting time")
        self.a.plot(data[2], label="Summary time")
        self.a.set_ylabel("Время, c")
        self.a.set_xlabel("Номер песни")
        self.a.set_xlim([0, (len(data[2])-1)])
        self.a.set_ylim([0, data[2][-1]])
        self.a.set_title("")
        self.a.text((len(data[2])-1) * (1 + config.text_x),
                    (data[2][-1]) * (1 - config.fontsize * (0*config.font_delta/config.figsize[1]+config.text_y) ),
                    data[3], fontsize=config.fontsize)
        self.a.text((len(data[2])-1) * (1 + config.text_x),
                    (data[2][-1]) * (1 - config.fontsize * (1*config.font_delta/config.figsize[1]+config.text_y) ),
                    data[4], fontsize=config.fontsize)
        self.a.text((len(data[2])-1) * (1 + config.text_x),
                    (data[2][-1]) * (1 - config.fontsize * (2*config.font_delta/config.figsize[1]+config.text_y) ),
                    data[5], fontsize=config.fontsize)
        self.a.text((len(data[2])-1) * (1 + config.text_x),
                    (data[2][-1]) * (1 - config.fontsize * (3*config.font_delta/config.figsize[1]+config.text_y) ),
                    data[6], fontsize=config.fontsize)
        self.a.legend()
        self.canvas.draw()
