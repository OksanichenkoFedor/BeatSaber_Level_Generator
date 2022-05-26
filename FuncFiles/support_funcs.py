import time
import FuncFiles.config as config
import os
import traceback as tr
import shutil

def put_corr_time(frame, type):
    now_time = time.time()
    if type == "download":
        curr_time = now_time - config.downloading["start time"]
        delta_time = now_time - config.downloading["last time"]
        config.downloading["last time"] = now_time
    elif type == "convert":
        curr_time = now_time - config.converting["start time"]
        delta_time = now_time - config.converting["last time"]
        config.converting["last time"] = now_time
    elif type == "downconv":
        curr_time = now_time - config.downconving["start time"]
        delta_time = now_time - config.downconving["last time"]
        config.downconving["last time"] = now_time
    config.last_time = now_time
    curr_str = str(round(curr_time // 3600)) + ":"
    if round((curr_time // 60) % 60)>=10:
        curr_str+=str(round((curr_time // 60) % 60))
    else:
        curr_str+="0"+str(round((curr_time // 60) % 60))
    curr_str+=":"
    if round(curr_time % 60)>=10:
        curr_str+=str(round(curr_time % 60))
    else:
        curr_str+="0"+str(round(curr_time % 60))

    frame.ftime_lbl["text"] = "Полное время: " + curr_str
    frame.ltime_lbl["text"] = "Последнее время: " + str(round(delta_time, 1)) + " сек"


def fprint(message, type="to file", filename="../logs/full_log.txt"):
    if type=="to file":
        file = open(filename, "a")
        try:
            file.write(str(message)+"\n")
        except:
            pass
            #file.write("Can't write: " + str(tr.format_exc()) + " \n")
        file.close()
    else:
        pass


def clean():
    app_dir = os.listdir("../DataApplication")
    for file in app_dir:
        if ".tmp" in file:
            os.remove("../DataApplication/"+file)

def check_conv_and_clean():
    found = False
    files = os.listdir("../Data/Converted")
    for conv in files:
        curr_f = os.listdir("../Data/Converted/" + conv)
        if ['info.txt', 'song.npy', 'SongInfo.txt', 'TextLevel.txt'] != curr_f:
            shutil.rmtree("../Data/Converted/" + conv)
            fprint("Remove last converted (was problem with C-code)")
            found = True
    return found
