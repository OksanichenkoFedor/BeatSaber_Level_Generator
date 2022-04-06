import os
from tkinter import Tk, W, E, BOTH, ttk, messagebox, BOTTOM, RIGHT, TOP
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton
import threading
import time
import FuncFiles.config as config
from FuncFiles.unzipp import unzip_new


def converting(frame):
    num = 0
    A = os.listdir("Downloads")
    frame.progress["max"] = len(A)
    while config.converting["permitted"]:
        config.converting["started"] = True
        # полезная нагрузка
        unzip_new("Downloads")
        frame.progress["value"] = num + 1
        num+=1

        frame.info_lbl["text"] = str(num) + " из " + str(frame.progress["max"])
        config.converting["started"] = False
        for key in config.conv_logs:
            config.conv_logs[key] = "-"

    frame.conv_but["text"] = "Конвертация"
    frame.info_lbl["text"] = "Пусто"


class DataWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")
        # self.pack(fill=BOTH, expand=True, side=RIGHT)

        self.columnconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.download = DownloadingWindow(self)
        self.convert = ConvertingWindow(self)
        #self.download.grid(row=0, column=0, padx=10, pady=10)
        self.convert.grid(row=0, column=1, padx=10, pady=10)


class DownloadingWindow(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")

        self.columnconfigure(1, pad=10)
        self.rowconfigure(2, pad=50)
        self.tot_lbl = Label(self, text="Шкала прогресса")
        self.tot_lbl.grid(row=0, column=0, columnspan=2)
        self.progress = ttk.Progressbar(self, orient="horizontal", maximum=200, mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=2)
        self.count_but = Button(self, text="Загрузка", command=self.compile)
        self.count_but.grid(row=2, column=0, columnspan=2)

    def compile(self):
        print("Download compile")


class ConvertingWindow(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")

        self.columnconfigure(1, pad=10)
        self.rowconfigure(5, pad=50)
        self.head_lbl = Label(self, text="Конвертация")
        self.head_lbl.grid(row=0, column=0, columnspan=2)
        self.progress = ttk.Progressbar(self, orient="horizontal", maximum=20, mode="determinate", length=200)
        self.progress.grid(row=1, column=0, columnspan=2)
        self.info_lbl = Label(self, text="Пусто")
        self.info_lbl.grid(row=2, column=0, columnspan=2)
        self.conv_but = Button(self, text="Конвертация", command=self.compile)
        self.conv_but.grid(row=3, column=0, columnspan=2, pady=10)
        self.log_but = Button(self, text="Логи", command=self.print_logs)
        self.log_but.grid(row=4, column=0, columnspan=2, pady=10)

    def compile(self):
        if config.converting["permitted"]:
            config.converting["permitted"] = False
        else:
            # очистка от пустых потоков
            num = len(config.threads) - 1
            while num >= 0:
                if not config.threads[num].isAlive():
                    config.threads.pop(num)
                num -= 1
            config.converting["permitted"] = True
            t = threading.Thread(target=converting, args=(self,))
            config.threads.append(t)
            config.converting["num_thread"] = len(config.threads) - 1
            #print("---")
            #print(len(config.threads))
            #print("---")
            t.start()
            self.conv_but["text"] = "Остановка"

    def print_logs(self):
        print("Пустой лог")


for key in config.conv_logs:
    print(key)