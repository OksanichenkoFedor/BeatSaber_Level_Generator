import os
import pickle
import numpy as np

class DataLogger():
    def __init__(self):
        self.load()

    def load(self):
        self.down = {
            "time": {"deltas": [], "full": [0], "new": []}
        }

        self.conv = {
            "time": {"deltas": [], "full": [0], "new": []}
        }
        file = open("../logs/downloading.txt", "r")
        full_time = 0
        for line in file.readlines():
            #print(line)
            if line == "-\n":
                self.down["time"]["full"].append(full_time)
            else:
                delta = float(line)
                self.down["time"]["deltas"].append(delta)
                full_time += delta
                self.down["time"]["full"].append(full_time)
        file.close()
        file = open("../logs/converting.txt", "r")
        full_time = 0
        for line in file.readlines():
            #print(line)
            if line == "-\n":
                self.conv["time"]["full"].append(full_time)
            else:
                delta = float(line)
                self.conv["time"]["deltas"].append(delta)
                full_time += delta
                self.conv["time"]["full"].append(full_time)
        file.close()


    def save(self):
        file = open("../logs/downloading.txt", "a")
        for i in range(len(self.down["time"]["new"])):
            file.write(str(self.down["time"]["new"][i]) + "\n")
        file.close()
        self.down["time"]["new"] = []
        file = open("../logs/converting.txt", "a")
        for i in range(len(self.conv["time"]["new"])):
            file.write(str(self.conv["time"]["new"][i]) + "\n")
        self.conv["time"]["new"] = []
        file.close()
        #print("save")

    def add(self, type, value, is_correct):
        if type[0] == "down":
            if type[1] == "time":
                if is_correct:
                    self.down["time"]["full"].append(self.down["time"]["full"][-1] + value)
                    self.down["time"]["new"].append(value)
                    self.down["time"]["deltas"].append(value)
                else:
                    self.down["time"]["full"].append(self.down["time"]["full"][-1])
                    self.down["time"]["new"].append("-")
        elif type[0] == "conv":
            if type[1] == "time":
                if is_correct:
                    self.conv["time"]["full"].append(self.conv["time"]["full"][-1] + value)
                    self.conv["time"]["new"].append(value)
                    self.conv["time"]["deltas"].append(value)
                else:
                    self.conv["time"]["full"].append(self.conv["time"]["full"][-1])
                    self.conv["time"]["new"].append("-")
        self.save()

    def get_plot_time(self):
        down = np.array(self.down["time"]["full"])
        conv = np.array(self.conv["time"]["full"])
        if down.shape!=conv.shape:
            print("---")
            print("Разные времена")
            print("---")
        all = down + conv
        label1 = "Среднее время загрузки: "+str(round(np.array(self.down["time"]["deltas"]).mean(), 2))+" c."
        label2 = "Среднее время обработки: " + str(round(np.array(self.conv["time"]["deltas"]).mean(), 1))+" c."
        label3 = "Количество обработанных песен: " + str(len(self.conv["time"]["full"]))
        label4 = "Количество полученных пар: " + str(len(os.listdir("../Data/Converted")))
        return down, conv, all, label1, label2, label3, label4