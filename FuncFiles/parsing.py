import os

from bs4 import BeautifulSoup
import requests
import lxml
import re
import wget
from tqdm.autonotebook import tqdm
import FuncFiles.config as config
from FuncFiles.support_funcs import fprint
from FuncFiles.support_funcs import put_corr_time





def parse_page(num, verbose=0):
    url = "https://bsaber.com/songs/page/" + str(num) + "/"
    try:
        response = requests.get(url)

    except:
        fprint("Данная страница не существует: " + url)
        print("Данная страница не существует: " + url)
        return 0
    soup = BeautifulSoup(response.text, 'lxml')

    mydivs = soup.find_all("a")
    urls = []
    for txt in mydivs:
        if ('href' in txt.attrs) and ('class' in txt.attrs):
            if '-download-zip' in txt['class']:
                urls.append(txt['href'])

    ans = "Страница номер " + str(num) + " обработана. Найдено " + str(len(urls)) + " песен"
    fprint(ans)
    return urls

    # print(mydivs)


def update_info_files():
    file = open("../Data/InfoFiles/downloaded.txt", "r")
    config.downloaded = file.readlines()
    file.close()
    file = open("../Data/InfoFiles/bad_dl.txt", "r")
    config.bad_dl = file.readlines()
    file.close()

    for i in range(len(config.bad_dl)):
        if config.bad_dl[i][-1:] == "\n":
            config.bad_dl[i] = config.bad_dl[i][:-1]
    for i in range(len(config.downloaded)):
        if config.downloaded[i][-1:] == "\n":
            config.downloaded[i] = config.downloaded[i][:-1]


def download_all(num=10000, verbose=0):
    num_error = 0

    update_info_files()

    for i in tqdm(range(num)):
        config.downloading["started"] = True
        download_page(i, verbose)
        config.downloading["started"] = False


def download_page(num, verbose, add_frame=False, frame=None):
    if add_frame:
        config.dl_logs["current operation"] = "Изучение страницы"
        frame.curr_act_lbl["text"] = "Изучение страницы"

    urls = parse_page(num, verbose=verbose)
    if verbose == 1:
        for ind in tqdm(range(len(urls))):
            url = urls[ind]
            single_download(url, verbose, add_frame, frame, i=ind, length=len(urls))
    else:
        for ind in range(len(urls)):
            url = urls[ind]
            single_download(url, verbose, add_frame, frame, i=ind, length=len(urls))



def single_download(url, frame, logger, i=0, length=0):
    if not ((url in config.downloaded) or (url in config.bad_dl)):

        frame.info_down_lbl["text"] = str(i + 1) + " из " + str(length)
        fprint("Try to download: " + url)
        try:
            config.dl_logs["current operation"] = "Скачивание: " + str(url)
            frame.curr_act_lbl["text"] = "Скачивание: " + str(url)
            wget.download(url, '../Data/Downloads')
            file = open("../Data/InfoFiles/downloaded.txt", "a")
            file.write(url + "\n")
            file.close()
            logger.info["downloaded"]["good"]["num"]+=1
            logger.info["downloaded"]["good"]["arr"].append(url)
            config.downloaded.append(url)
            fprint("Correct download: " + url)
            return True
        except Exception as e:
            print()
            print(e)
            print("Проблема с " + url)
            fprint("Fail in downloading: " + url)
            fprint("Error: " + str(e))
            # print(os.listdir("../Data/InfoFiles/"))
            file = open("../Data/InfoFiles/bad_dl.txt", "a")
            file.write(url + "\n")
            file.close()
            logger.info["downloaded"]["bad"]["num"] += 1
            logger.info["downloaded"]["bad"]["arr"].append(url)
            config.bad_dl.append(url)
            config.bad_downloaded += 1
            frame.bad_d_lbl["text"] = "Количество плохих загрузок: " + str(config.bad_downloaded)
            return False
    else:
        fprint(url+" is already done")
        return "already_done"

