import os

from bs4 import BeautifulSoup
import requests
import lxml
import re
import wget
from tqdm.autonotebook import tqdm
import FuncFiles.config as config
from FuncFiles.support_funcs import put_corr_time





def parse_page(num, verbose=0):
    url = "https://bsaber.com/songs/page/" + str(num) + "/"
    try:
        response = requests.get(url)
    except:
        print("Данная страница не существует")
        return 0
    soup = BeautifulSoup(response.text, 'lxml')

    mydivs = soup.find_all("a")
    urls = []
    for txt in mydivs:
        if ('href' in txt.attrs) and ('class' in txt.attrs):
            if '-download-zip' in txt['class']:
                urls.append(txt['href'])

    if verbose == 1:
        ans = "Страница номер " + str(num) + " обработана. Найдено " + str(len(urls)) + " песен"
        print(ans)
    else:
        if len(urls) != 20:
            print("Ахтунг!!!")
    return urls

    # print(mydivs)


def update_info_files():
    file = open("InfoFiles/downloaded.txt", "r")
    config.downloaded = file.readlines()
    file.close()
    file = open("InfoFiles/bad_dl.txt", "r")
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
        for url in tqdm(urls):
            if not ((url in config.downloaded) or (url in config.bad_dl)):
                try:
                    wget.download(url, 'Downloads')
                    file = open("InfoFiles/downloaded.txt", "a")
                    file.write(url + "\n")
                    file.close()
                    config.downloaded.append(url)
                except:
                    print()
                    print("Проблема с " + url)
                    file = open("InfoFiles/bad_dl.txt", "a")
                    file.write(url + "\n")
                    file.close()
                    config.bad_dl.append(url)
    else:
        for i in range(len(urls)):
            url = urls[i]
            if not ((url in config.downloaded) or (url in config.bad_dl)):
                if add_frame:
                    frame.info_down_lbl["text"] = str(i+1) + " из " + str(len(urls))
                try:
                    if add_frame:
                        config.dl_logs["current operation"] = "Скачивание: " + str(url)
                        frame.curr_act_lbl["text"] = "Скачивание: " + str(url)
                    wget.download(url, 'Downloads')
                    file = open("InfoFiles/downloaded.txt", "a")
                    file.write(url + "\n")
                    file.close()
                    config.downloaded.append(url)
                    if add_frame:
                        put_corr_time(frame, "download")
                except:
                    print()
                    print("Проблема с " + url)
                    file = open("InfoFiles/bad_dl.txt", "a")
                    file.write(url + "\n")
                    file.close()
                    config.bad_dl.append(url)
                    if add_frame:
                        config.bad_downloaded += 1
                        frame.bad_lbl["text"] = "Количество плохих загрузок: " + str(config.bad_downloaded)
