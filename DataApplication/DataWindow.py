import os
from tkinter import Tk, W, E, BOTH, ttk, messagebox, BOTTOM, RIGHT, TOP
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton
import threading
import time
import FuncFiles.config as config
from FuncFiles.unzipp import unzip_new
from FuncFiles.parsing import download_page, parse_page, single_download
from FuncFiles.support_funcs import put_corr_time
from DataApplication.logger import DataLogger
from DataApplication.plot import PlotFrame


def converting(frame):
    num = 0
    A = os.listdir("../Data/Downloads")
    frame.progress["max"] = len(A)
    config.converting["start time"] = time.time()
    config.converting["last time"] = time.time()
    frame.info_lbl["text"] = str(num+1) + " из " + str(frame.progress["max"])
    while config.converting["permitted"]:
        config.converting["started"] = True

        unzip_new("../Data/Downloads", frame=frame)
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


def downconving(frame):
    num = config.downconving["start number"]
    frame.main_progress["value"] = 0
    frame.main_progress["max"] = config.downconving["end number"] - config.downconving["start number"]
    frame.info_lbl["text"] = str(num + 1 - config.downconving["start number"])\
                             + " из " + str(config.downconving["end number"] -
                             config.downconving["start number"])
    config.downconving["start time"] = time.time()
    config.downconving["last time"] = time.time()
    while config.downconving["permitted"] and (num < config.downconving["end number"]):
        config.downconving["started"] = True
        config.dl_logs["current operation"] = "Изучение страницы"
        frame.curr_act_lbl["text"] = "Изучение страницы"
        urls = parse_page(num, verbose=0)
        frame.page_progress["max"] = len(urls)
        frame.page_progress["value"] = 0
        ind = 0
        while config.downconving["permitted"] and (ind < len(urls)):
            url = urls[ind]
            frame.page_progress["value"] = ind

            config.downconving["downloading"] = True
            curr_start1 = time.time()
            res = single_download(url, 0, True, frame, i=ind, length=len(urls))
            curr_end1 = time.time()
            config.downconving["downloading"] = False
            #if res!="already_done":
            if res==True:
                print(res)


                config.downconving["converting"] = True
                curr_start2 = time.time()
                res1 = unzip_new("../Data/Downloads", frame=frame)
                curr_end2 = time.time()
                res2 = res1 and res
                frame.parent.logger.add(["down", "time"], curr_end1 - curr_start1, res2)
                frame.parent.logger.add(["conv", "time"], curr_end2-curr_start2, res2)
                config.downconving["converting"] = False

            put_corr_time(frame, "downconv")
            frame.page_progress["value"] = ind+1
            ind+=1
            frame.parent.plot.replot()



        frame.info_lbl["text"] = str(num + 1 - config.downconving["start number"]) + \
                                 " из " + str(config.downconving["end number"] -
                                 config.downconving["start number"])
        frame.info_down_lbl["text"] = "0 из 0"
        config.downconving["started"] = False
        num += 1
        frame.parent.logger.save()

        frame.page_progress["value"] = 0
        frame.main_progress["value"] = num - config.downconving["start number"]

    frame.dl_but["text"] = "Загрузка"
    frame.info_lbl["text"] = "-Пусто-"
    frame.info_down_lbl["text"] = "-Пусто-"
    frame.curr_act_lbl["text"] = "-Пусто-"
    config.downloading["permitted"] = False


class DataWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Обработчик данных")
        self.pack(fill=BOTH, expand=True)


        self.columnconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.logger = DataLogger()
        self.plot = PlotFrame(self)
        self.downconv = DownloadConvertWin(self)
        #self.plot.grid(row=0, column=0, padx=10, pady=10)
        #self.downconv.grid(row=0, column=1, padx=10, pady=10)
        self.plot.pack()
        self.downconv.pack()
        self.plot.replot()


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
                if not config.threads[num].is_alive():
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
                if not config.threads[num].is_alive():
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


class DownloadConvertWin(Frame):
    def __init__(self, parent):
        self.parent = parent

        super().__init__()
        self.initUI()

    def initUI(self):

        self.start_page = tk.StringVar()
        self.start_page.set(str(config.downconving["start number"]))
        self.end_page = tk.StringVar()
        self.end_page.set(str(config.downconving["end number"]))

        self.columnconfigure(4, pad=10)
        self.rowconfigure(12, pad=50)
        self.tot_lbl = Label(self, text="Загрузка/Конвертация")
        self.tot_lbl.grid(row=0, column=0, columnspan=2,pady=20)
        self.main_progress = ttk.Progressbar(self, orient="horizontal", maximum=200, mode="determinate", length=300)
        self.main_progress.grid(row=1, column=0, columnspan=2)
        self.info_lbl = Label(self, text="-Пусто-")
        self.info_lbl.grid(row=2, column=0, columnspan=2)
        self.st_pg_lbl = Label(self, text="Первая страница")
        self.st_pg_lbl.grid(row=3, column=0, padx=10, pady=20)
        self.st_ent = tk.Entry(self, textvariable=self.start_page)
        self.st_ent.grid(row=3, column=1, padx=10, pady=20)
        self.end_pg_lbl = Label(self, text="Последняя страница")
        self.end_pg_lbl.grid(row=4, column=0, padx=10, pady=20)
        self.end_ent = tk.Entry(self, textvariable=self.end_page)
        self.end_ent.grid(row=4, column=1, padx=10, pady=20)
        self.page_progress = ttk.Progressbar(self, orient="horizontal", maximum=200, mode="determinate", length=100)
        self.page_progress.grid(row=5, column=0, columnspan=2)
        self.info_down_lbl = Label(self, text="-Пусто-")
        self.info_down_lbl.grid(row=6, column=0, columnspan=2)
        self.ftime_lbl = Label(self, text="Полное время: 0")
        self.ftime_lbl.grid(row=7, column=0, columnspan=2)
        self.ltime_lbl = Label(self, text="Последнее время: 0")
        self.ltime_lbl.grid(row=8, column=0, columnspan=2)
        self.curr_act_lbl = Label(self, text="-Пусто-")
        self.curr_act_lbl.grid(row=9, column=0, columnspan=2)
        self.bad_d_lbl = Label(self, text="Количество плохих загрузок: " + str(config.bad_downloaded))
        self.bad_d_lbl.grid(row=10, column=0, columnspan=2)
        self.bad_z_lbl = Label(self, text="Количество плохих обработок: " + str(config.bad_zipped))
        self.bad_z_lbl.grid(row=11, column=0, columnspan=2)
        self.dl_but = Button(self, text="Загрузка", command=self.compile)
        self.dl_but.grid(row=12, column=0, columnspan=2)


        self.start_page.trace('w',self.change_pages)
        self.end_page.trace('w', self.change_pages)


    def compile(self):
        if config.downconving["permitted"]:
            config.downconving["permitted"] = False
        else:
            # очистка от пустых потоков
            num = len(config.threads) - 1
            while num >= 0:
                if not config.threads[num].is_alive():
                    config.threads.pop(num)
                num -= 1
            config.downconving["permitted"] = True
            t = threading.Thread(target=downconving, args=(self,))
            config.threads.append(t)
            config.downconving["num_thread"] = len(config.threads) - 1
            t.start()
            self.dl_but["text"] = "Остановка"

    def change_pages(self, *args):
        print("sdsdsdsdsd")
        #self.main_progress["max"] = config.downconving["end number"] - config.downconving["start number"]
        old_st = config.downconving["start number"]
        old_end = config.downconving["end number"]
        good_values = True
        try:
            new_st = int(self.start_page.get())
            new_end = int(self.end_page.get())
            if new_st < self.main_progress["value"]:
                good_values = False
            if new_st > new_end:
                good_values = False
        except:
            good_values = False
        if good_values:
            config.downconving["end number"] = new_end
            config.downconving["start number"] = new_st
            self.main_progress["max"] = config.downconving["end number"] - config.downconving["start number"]
            self.main_progress["value"] = self.main_progress["value"] + old_st - new_st


