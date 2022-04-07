import os
from tkinter import Tk, W, E, BOTH, ttk, messagebox, BOTTOM, RIGHT, TOP
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton
import threading
import time
import FuncFiles.config as config
from FuncFiles.unzipp import unzip_new



def put_corr_time(frame):
    now_time = time.time()
    curr_time = now_time - config.start_time
    delta_time = now_time - config.last_time
    config.last_time = now_time
    curr_str = str(round(curr_time//3600))+":"+str(round((curr_time//60)%60))+":"+str(round(curr_time%60))
    frame.ftime_lbl["text"] = "Полное время: "+curr_str
    frame.ltime_lbl["text"] = "Последнее время: "+str(round(delta_time, 1))+" сек"



def converting(frame):
    num = 0
    A = os.listdir("Downloads")
    frame.progress["max"] = len(A)
    config.start_time = time.time()
    config.last_time = time.time()
    while config.converting["permitted"]:
        config.converting["started"] = True


        unzip_new("Downloads",frame = frame)
        frame.progress["value"] = num + 1
        num+=1

        frame.info_lbl["text"] = str(num) + " из " + str(frame.progress["max"])
        config.converting["started"] = False
        put_corr_time(frame)
        for key in config.conv_logs:
            config.conv_logs[key] = "-"

    frame.conv_but["text"] = "Конвертация"
    frame.info_lbl["text"] = "-Пусто-"
    frame.song_name_lbl["text"] = "-Пусто-"
    frame.curr_act_lbl["text"] = "-Пусто-"
    config.bad_zipped = 0



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
            #print("---")
            #print(len(config.threads))
            #print("---")
            t.start()
            self.conv_but["text"] = "Остановка"

    def print_logs(self):
        for key in config.conv_logs:
            print(key + ": "+str(config.conv_logs[key]))


