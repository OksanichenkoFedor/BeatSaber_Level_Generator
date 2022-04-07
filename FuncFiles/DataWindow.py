import os
from tkinter import Tk, W, E, BOTH, ttk, messagebox, BOTTOM, RIGHT, TOP
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton
import threading
import time
import FuncFiles.config as config
from FuncFiles.unzipp import unzip_new
from FuncFiles.parsing import download_page
from FuncFiles.support_funcs import put_corr_time


def converting(frame):
    num = 0
    A = os.listdir("Downloads")
    frame.progress["max"] = len(A)
    config.converting["start time"] = time.time()
    config.converting["last time"] = time.time()
    frame.info_lbl["text"] = str(num+1) + " из " + str(frame.progress["max"])
    while config.converting["permitted"]:
        config.converting["started"] = True

        unzip_new("Downloads", frame=frame)
        frame.progress["value"] = num + 1
        num += 1

        frame.info_lbl["text"] = str(num) + " из " + str(frame.progress["max"])
        config.converting["started"] = False
        put_corr_time(frame, "convert")
        for key in config.conv_logs:
            config.conv_logs[key] = "-"

    frame.conv_but["text"] = "Конвертация"
    frame.info_lbl["text"] = "-Пусто-"
    frame.song_name_lbl["text"] = "-Пусто-"
    frame.curr_act_lbl["text"] = "-Пусто-"
    config.converting["permitted"] = False
    config.bad_zipped = 0


def downloading(frame):
    #print("s1")
    num = config.downloading["start number"]
    frame.progress["value"] = 0
    frame.progress["max"] = config.downloading["end number"] - config.downloading["start number"]
    frame.info_lbl["text"] = str(num+1) + " из " + str(config.downloading["end number"] -
                                                     config.downloading["start number"])
    config.downloading["start time"] = time.time()
    config.downloading["last time"] = time.time()
    while config.downloading["permitted"] and (num < config.downloading["end number"]):
        config.downloading["started"] = True
        download_page(num, verbose=0, add_frame=True, frame=frame)
        frame.info_lbl["text"] = str(num+1) + " из " + str(config.downloading["end number"] -
                                                         config.downloading["start number"])
        frame.info_down_lbl["text"] = "0 из 0"
        config.downloading["started"] = False
        num += 1
        frame.progress["value"] = num - config.downloading["start number"]

    frame.dl_but["text"] = "Загрузка"
    frame.info_lbl["text"] = "-Пусто-"
    frame.info_down_lbl["text"] = "-Пусто-"
    frame.curr_act_lbl["text"] = "-Пусто-"
    config.downloading["permitted"] = False
    print("s2")


class DataWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")

        self.columnconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.convert = ConvertingWindow(self)
        self.convert.grid(row=0, column=1, padx=10, pady=10)
        self.download = DownloadingWindow(self)
        self.download.grid(row=0, column=0, padx=10, pady=10)


class DownloadingWindow(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")

        self.columnconfigure(1, pad=10)
        self.rowconfigure(10, pad=50)
        self.tot_lbl = Label(self, text="Загрузка")
        self.tot_lbl.grid(row=0, column=0, columnspan=2)
        self.progress = ttk.Progressbar(self, orient="horizontal", maximum=200, mode="determinate", length=300)
        self.progress.grid(row=1, column=0, columnspan=2)
        self.info_lbl = Label(self, text="-Пусто-")
        self.info_lbl.grid(row=2, column=0, columnspan=2)
        self.info_down_lbl = Label(self, text="-Пусто-")
        self.info_down_lbl.grid(row=3, column=0, columnspan=2)
        self.ftime_lbl = Label(self, text="Полное время: 0")
        self.ftime_lbl.grid(row=4, column=0, columnspan=2)
        self.ltime_lbl = Label(self, text="Последнее время: 0")
        self.ltime_lbl.grid(row=5, column=0, columnspan=2)
        self.curr_act_lbl = Label(self, text="-Пусто-")
        self.curr_act_lbl.grid(row=6, column=0, columnspan=2)
        self.bad_lbl = Label(self, text="Количество плохих загрузок: "+str(config.bad_downloaded))
        self.bad_lbl.grid(row=7, column=0, columnspan=2)
        self.dl_but = Button(self, text="Загрузка", command=self.compile)
        self.dl_but.grid(row=8, column=0, columnspan=2)

    def compile(self):
        if config.downloading["permitted"]:
            config.downloading["permitted"] = False
        else:
            # очистка от пустых потоков
            num = len(config.threads) - 1
            while num >= 0:
                if not config.threads[num].isAlive():
                    config.threads.pop(num)
                num -= 1
            config.downloading["permitted"] = True
            t = threading.Thread(target=downloading, args=(self,))
            config.threads.append(t)
            config.downloading["num_thread"] = len(config.threads) - 1
            t.start()
            self.dl_but["text"] = "Остановка"


class ConvertingWindow(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")

        self.columnconfigure(1, pad=10)
        self.rowconfigure(10, pad=50)
        self.head_lbl = Label(self, text="Конвертация")
        self.head_lbl.grid(row=0, column=0, columnspan=2)
        self.progress = ttk.Progressbar(self, orient="horizontal", maximum=20, mode="determinate", length=300)
        self.progress.grid(row=1, column=0, columnspan=2)
        self.info_lbl = Label(self, text="-Пусто-")
        self.info_lbl.grid(row=2, column=0, columnspan=2)
        self.ftime_lbl = Label(self, text="Полное время: 0")
        self.ftime_lbl.grid(row=3, column=0, columnspan=2)
        self.ltime_lbl = Label(self, text="Последнее время: 0")
        self.ltime_lbl.grid(row=4, column=0, columnspan=2)
        self.curr_act_lbl = Label(self, text="-Пусто-")
        self.curr_act_lbl.grid(row=5, column=0, columnspan=2)
        self.song_name_lbl = Label(self, text="-Пусто-")
        self.song_name_lbl.grid(row=6, column=0, columnspan=2)
        self.bad_lbl = Label(self, text="Количество плохих песен: 0")
        self.bad_lbl.grid(row=7, column=0, columnspan=2)
        self.conv_but = Button(self, text="Конвертация", command=self.compile)
        self.conv_but.grid(row=8, column=0, columnspan=2, pady=20)
        self.log_but = Button(self, text="Логи", command=self.print_logs)
        self.log_but.grid(row=9, column=0, columnspan=2, pady=20)

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
            # print("---")
            # print(len(config.threads))
            # print("---")
            t.start()
            self.conv_but["text"] = "Остановка"

    def print_logs(self):
        for key in config.conv_logs:
            print(key + ": " + str(config.conv_logs[key]))
