
threads = []
number_of_download_process = 0
number_of_convert_process = 0
downloading = {"permitted" :False, "started" :False, "num_thread" :0}
converting = {"permitted" :False, "started" :False, "num_thread" :0}

conv_logs = {
    "song name": "-",
    "current operation": "-",
    "beat": "-",
}

bad_zipped = 0

start_time = 0
last_time = 0


cont_working = False
num = 10
