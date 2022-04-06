import os

from bs4 import BeautifulSoup
import requests
import lxml
import re
import wget
from tqdm.autonotebook import tqdm


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


def download_all(num=10000, verbose=0):
    num_error = 0
    file = open("InfoFiles/downloaded.txt", "r")
    downloaded = file.readlines()
    file.close()
    file = open("InfoFiles/bad_dl.txt", "r")
    bad_dl = file.readlines()
    file.close()

    for i in range(len(bad_dl)):
        if bad_dl[i][-1:]=="\n":
            bad_dl[i] = bad_dl[i][:-1]
    for i in range(len(downloaded)):
        if downloaded[i][-1:]=="\n":
            downloaded[i] = downloaded[i][:-1]

    for i in tqdm(range(num)):
        urls = parse_page(i, verbose=verbose)
        for url in tqdm(urls):
            if not ((url in downloaded) or (url in bad_dl)):
                try:
                    wget.download(url, 'Downloads')
                    file = open("InfoFiles/downloaded.txt", "a")
                    file.write(url+"\n")
                    file.close()
                    downloaded.append(url)
                except:
                    print()
                    print("Проблема с "+url)
                    file = open("InfoFiles/bad_dl.txt", "a")
                    file.write(url + "\n")
                    file.close()
                    bad_dl.append(url)



