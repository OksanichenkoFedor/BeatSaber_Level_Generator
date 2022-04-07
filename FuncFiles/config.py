
threads = []
number_of_download_process = 0
number_of_convert_process = 0
downloading = {
    "permitted" :False,
    "started" :False,
    "num_thread" :0,
    "start number": 0,
    "end number": 10000,
    "start time" :0,
    "last time" :0
}

converting = {
    "permitted" :False,
    "started" :False,
    "num_thread" :0,
    "start time" :0,
    "last time" :0
}

conv_logs = {
    "song name": "-",
    "current operation": "-",
    "beat": "-",
}

dl_logs = {
    "url": "-",
    "current operation": "-"
}

bad_zipped = 0
bad_downloaded = 0


downloaded = []
bad_dl = []


cont_working = False
num = 10
