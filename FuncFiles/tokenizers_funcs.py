import mg_tok
import os
from tqdm.autonotebook import tqdm
import numpy as np
import matplotlib.pyplot as plt
import time
import shutil


def make_tokenizer():
    while True:
        try:
            converted = os.listdir("../Data/Converted")
            texts = []
            for i in tqdm(range(len(converted))):
                file = open("../Data/Converted/" + converted[i] + "/TextLevel.txt", 'r')
                curr = file.read()
                curr = curr.split(" ")
                curr = np.array(curr)
                curr = curr.astype("int")
                texts.append(curr)

            min_el = -1
            max_el = 0
            bad_t = texts[0]
            for text in texts:
                for el in text:
                    if el < min_el:
                        bad_t = text
                    max_el = max(max_el, el)
                    min_el = min(min_el, el)

            if min_el != -1:
                print("Проблема")
                return False

            text_tokenizer = mg_tok.MultigrammTokenizer()

            return text_tokenizer, texts
        except:
            time.sleep(0.5)


def plot_curr_hist():
    while True:
        try:
            converted = os.listdir("../Data/Converted")
            Beats = []
            Len = []
            for i in range(len(converted)):
                file = open("../Data/Converted/" + converted[i] + "/SongInfo.txt", 'r')
                curr = (file.readline()).split(" ")
                beat = float(curr[0])
                length = int(curr[1])
                Len.append(length)
                Beats.append(60.0 / beat)
                file.close()
            plt.hist(Len, bins=40)
            plt.plot()
            return True
        except Exception as e:
            print(e)
            pass


def make_ML_data(tokenizer, max_num=-1):
    converted = os.listdir("../Data/Converted")
    if max_num == -1:
        max_num = len(converted)

    for i in tqdm(range(max_num)):
        shutil.copytree("../Data/Converted/" + converted[i], "../Data/MLData/" + converted[i])
        try:
            file = open("../Data/MLData/" + converted[i] + "/TextLevel.txt", 'r')
            curr = file.read()
            curr = curr.split(" ")
            curr = np.array(curr)
            curr = curr.astype("int")
            file.close()
            tokened = tokenizer.tokenize(curr, make_drop=True, prob=0.001)
            num_end = 0
            for tok in tokened:
                if tok == 2:
                    num_end += 1
            if (num_end > 1) or (num_end == 0):
                print("Конечный токен размещён неправильно")
            file = open("../Data/MLData/" + converted[i] + "/TokenLevel.txt", 'w')
            file.write(" ".join(np.array(tokened).astype("str")))
            file.close()
            file = open("../Data/MLData/" + converted[i] + "/TokenLevel.txt", 'r')
            tokened_1 = file.read()
            tokened_1 = tokened_1.split(" ")
            tokened_1 = np.array(tokened_1)
            tokened_1 = tokened_1.astype("int")
            file.close()
            if not (list(tokened_1) == list(tokened)):
                print("Несоответстие токенизированных версий: " + str(i))
            text_1 = tokenizer.detokenize(tokened_1)
            if not (list(text_1) == list(curr)):
                print("Несоответстие текстовых версий: " + str(i))
        except Exception as e:
            print(e)
            print("Пустая папка: " + converted[i])
