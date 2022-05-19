
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

downconving = {
    "permitted" :False,
    "started" :False,
    "downloading" :False,
    "converting" :False,
    "num_thread" :0,
    "start number": 0,
    "end number": 10000,
    "start time" :0,
    "last time" :0
}


bad_zipped = 0
bad_downloaded = 0


downloaded = []
bad_dl = []


cont_working = False
num = 10

fontsize = 10
font_delta = 0.03
figsize = (20, 7)
text_x = 0.01
text_y = 0.002
