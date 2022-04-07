import time
import FuncFiles.config as config

def put_corr_time(frame, type):
    now_time = time.time()
    if type == "download":
        curr_time = now_time - config.downloading["start time"]
        delta_time = now_time - config.downloading["last time"]
    elif type == "convert":
        curr_time = now_time - config.converting["start time"]
        delta_time = now_time - config.converting["last time"]
    config.last_time = now_time
    curr_str = str(round(curr_time // 3600)) + ":" + str(round((curr_time // 60) % 60)) + ":" + str(
        round(curr_time % 60))
    frame.ftime_lbl["text"] = "Полное время: " + curr_str
    frame.ltime_lbl["text"] = "Последнее время: " + str(round(delta_time, 1)) + " сек"