import numpy as np
from tqdm.autonotebook import tqdm
# import pickle5 as pickle
import pickle
import random
from FuncFiles.lang_converter import LangConverter


class MultigrammTokenizer:
    """
    This class is made to tokenize sequence of numbers

    field vocab: array with information about every gramm, every element identified with some number and
                 contains dictionary with current number ("num"); current token ("token"); boolean, which tells
                 is this gramm is in vocabulary. Also it conatins new vocab ("vocab"), which contains information
                 about gramms, which are starts with currecnt gramm
    field devoc: is dictionary, which matches gramms with token, to decode tokenised message
    field last_token: Current last added token
    field vocab_size: Current size of vocab
    field gramms: Array with all gramms
    field start_token: Token, which is added to the start of every message
    field end_token: Token, which is added to the start of every message
    field start_num: Contains length of start vocabulary (we need it when we do rebolance)

    method init: Just initalise
    method make_start_vocab: Make start vocab, gramms, devoc
    method giveNT: Give new token
    method adopt: Change vocabulary according to corpus of sequences, using some rules of evolution
    method count_start: Count frequences of every gramm in corpus of sequences
    method adopt_onse: Change vocabulary according to corpus of sequences
    method rebalance: Rebalanse tokeniser, after new tokens were added
    method makeNGW: Make cortege-array of new grams with their frequencies
    method adopt_NG: Add new gramm to self.vocab (with num)\
    method count_freq: Count freq of current gramm
    method tokenize: Tokenize corpus of sequences
    method correct_add: Tokenize and add new element of current sequence to tokenized massive
    method detokenize: Detokenize one sequence
    method sorted_devoc: Print sorted self.devoc
    method save: Save current tokenizer to folder (it must exist)
    method load: Load tokenizer from folder


    """

    def __init__(self, num=444):
        """

        :param num: Length of vocabulary (max number in sequence - 1)

        """
        self.vocab = {}
        self.devoc = {}
        self.last_token = 2
        self.vocab_size = 2
        self.start_voc = []
        self.gramms = []
        self.make_start_vocab(num)
        self.start_token = 1
        self.end_token = 2
        self.start_num = num

    def make_start_vocab(self, num):
        """

        Make start vocab, gramms, devoc

        :param num: Length of vocabulary (max number in sequence - 1)

        :return: Nothing

        """
        self.start_voc.append(-1)
        self.gramms.append([-1])
        curr_vok = {"num": 0, "token": self.giveNT(), "vocab": {}, "empty": False}
        self.devoc[curr_vok["token"]] = {"num": 0, "gramm": [-1]}
        self.vocab[-1] = curr_vok
        for i in range(num):
            self.start_voc.append(i)
            self.gramms.append([i])
            curr_vok = {"num": 0, "token": self.giveNT(), "vocab": {}, "empty": False}
            self.devoc[curr_vok["token"]] = {"num": 0, "gramm": [i]}
            self.vocab[i] = curr_vok

    def giveNT(self):
        """

        Give new token

        :return: new token (int)

        """
        self.last_token += 1
        self.vocab_size += 1
        return self.last_token

    def adopt(self, texts, vocab_size=2000, ad_num=False, num_cycles=10, part_add=0.25,
              verbose_main=False, verbose_NGW=True, min_len=0):
        """

        Change vocabulary according to corpus of sequences, using some rules of evolution

        :param min_len: Minimum length of gramms in vocabulary
        :param verbose_NGW: If true, there will appear tqdm progress bar in every "adopt_once", if false - no
        :param verbose_main: If true, there will appear tqdm progress bar in main loop, if false - no
        :param part_add: Part of new gramms, which must be added in every "adopt_onse"
        :param texts: Corpus of sequences, on which we will make tokenizer
        :param vocab_size: Aim of vocab size
        :param ad_num: Boolean, if True, then adding new "words" will be repeated exact number of times (num)
                                if False, then adding will continue, while vocab is not filled
        :param num_cycles: Number of adding cycles

        :return: Nothing

        """
        # str_texts = []
        # for text in texts:
        #    curr_text = text.copy()
        #    curr_text = ",".join(list(curr_text.astype(str)))
        #    str_texts.append(curr_text)
        # self.count_start(texts)
        if verbose_main:

            if ad_num:
                for i in tqdm(range(num_cycles)):
                    self.adopt_onse(texts, part_add, verbose=verbose_NGW, min_len=min_len)
            else:
                while self.vocab_size < vocab_size:
                    self.adopt_onse(texts, part_add, verbose=verbose_NGW, min_len=min_len)
        else:
            if ad_num:
                for i in range(num_cycles):
                    self.adopt_onse(texts, part_add, verbose=verbose_NGW, min_len=min_len)
            else:
                while self.vocab_size < vocab_size:
                    self.adopt_onse(texts, part_add, verbose=verbose_NGW, min_len=min_len)

    def count_start(self, texts):
        """

        Count frequencies of every gramm in corpus of sequences

        :param texts: Corpus of sequences

        :return: Nothing

        """
        keys = self.vocab.keys()
        for key in keys:
            self.vocab[key]["num"] = 0
        for text in texts:
            unique, counts = np.unique(text, return_counts=True)
            for i in range(len(unique)):
                self.vocab[unique[i]]["num"] += counts[i]
                token = self.vocab[unique[i]]["token"]
                self.devoc[token]["num"] += counts[i]

    def adopt_onse(self, texts, part_add=0.25, verbose=True, min_len=0):
        """

        Change vocabulary according to corpus of sequences

        :param texts: Corpus of sequences, on which we will make tokenizer
        :param part_add: Part of new gramms, which must be added
        :param verbose: If true, there will appear tqdm progress bar, if false - no
        :param min_len: Minimum length of gramms in vocabulary (use in rebolance)

        :return: Nothing

        """
        NG = self.makeNGW(texts, verbose)
        i = 0
        start_len = self.vocab_size
        while (i < int(start_len * part_add)) and (i < len(NG)):
            self.adopt_NG(NG[i][1], NG[i][0])
            i += 1
        for key in self.devoc.keys():
            self.devoc[key]["num"] = 0
        for text in texts:
            tokened = self.tokenize(text)
            for token in tokened[1:-1]:
                self.devoc[token]["num"] += 1
        self.rebalance(border=min_len)

    def rebalance(self, border=0):
        """

        Rebalanse tokeniser, after new tokens were added

        :param border: Minimum length of gramms in vocabulary (another except of quants will be deleted)

        :return: Nothing

        """
        old_devoc = self.devoc.copy()
        old_voc_size = self.vocab_size
        self.vocab = {}
        self.devoc = {}
        self.last_token = 2
        self.vocab_size = 2
        self.start_voc = []
        self.gramms = []
        self.make_start_vocab(self.start_num)
        self.start_token = 1
        self.end_token = 2
        ind = 3
        while ind <= old_voc_size:
            curr_num = old_devoc[ind]["num"]
            curr_gramm = old_devoc[ind]["gramm"]
            if (curr_num > border) and (len(curr_gramm) > 1):
                self.adopt_NG(curr_gramm, curr_num)
            elif len(curr_gramm) == 1:
                self.vocab[curr_gramm[0]]["num"] = curr_num
                self.devoc[self.vocab[curr_gramm[0]]["token"]]["num"] = curr_num

            ind += 1

    def makeNGW(self, texts, verbose):
        """

        Make cortege-array of new grams with their frequencies

        :param texts: Corpus of sequences, on which we adopted tokenizer
        :param verbose: If true, there will appear tqdm progress bar, if false - no

        :return: Sorted array of new gramms, which are possible to add with their frequencies

        """

        if verbose:
            print("---")
            tokened = []
            for i in tqdm(range(len(texts))):
                tokened.append(self.tokenize(texts[i])[1:-1])
            new_gramms = {}
            for key_1 in tqdm(self.devoc.keys()):
                for key_2 in self.devoc.keys():
                    gramm1 = self.devoc[key_1]["gramm"].copy()
                    gramm2 = self.devoc[key_2]["gramm"].copy()
                    curr_gramm = gramm1 + gramm2
                    if not (curr_gramm in self.gramms):
                        if int(key_1) in new_gramms:
                            new_gramms[int(key_1)][int(key_2)] = {"num": 0, "gramm": curr_gramm}
                        else:
                            new_gramms[int(key_1)] = {}
                            new_gramms[int(key_1)][int(key_2)] = {"num": 0, "gramm": curr_gramm}
            for i in tqdm(range(len(tokened))):
                for ind in range(1, len(tokened[i])):
                    tok1 = tokened[i][ind - 1]
                    tok2 = tokened[i][ind]
                    try:
                        new_gramms[tok1][tok2]["num"] += 1
                    except:
                        print(tok1)
                        print(tok2)
                        print(self.devoc[tok1]["gramm"].copy())
                        print(self.devoc[tok2]["gramm"].copy())
                        a = self.devoc[tok1]["gramm"].copy() + self.devoc[tok2]["gramm"].copy()
                        print(a)
                        print(a in self.gramms)
                        print(texts[i])
                        print(i)
                        new_gramms[tok1][tok2]["num"] += 1
            ngrams = []
            for key_1 in new_gramms.keys():
                for key_2 in new_gramms[key_1].keys():
                    ngrams.append((new_gramms[key_1][key_2]["num"], new_gramms[key_1][key_2]["gramm"]))
            ngrams = sorted(ngrams, reverse=True)
            return ngrams
        else:
            tokened = []
            for i in range(len(texts)):
                tokened.append(self.tokenize(texts[i])[1:-1])
            new_gramms = {}
            for key_1 in self.devoc.keys():
                for key_2 in self.devoc.keys():
                    gramm1 = self.devoc[key_1]["gramm"].copy()
                    gramm2 = self.devoc[key_2]["gramm"].copy()
                    curr_gramm = gramm1 + gramm2
                    if not (curr_gramm in self.gramms):
                        if int(key_1) in new_gramms:
                            new_gramms[int(key_1)][int(key_2)] = {"num": 0, "gramm": curr_gramm}
                        else:
                            new_gramms[int(key_1)] = {}
                            new_gramms[int(key_1)][int(key_2)] = {"num": 0, "gramm": curr_gramm}
            for i in range(len(tokened)):
                for ind in range(1, len(tokened[i])):
                    tok1 = tokened[i][ind - 1]
                    tok2 = tokened[i][ind]
                    try:
                        new_gramms[tok1][tok2]["num"] += 1
                    except:
                        print(tok1)
                        print(tok2)
                        print(self.devoc[tok1]["gramm"].copy())
                        print(self.devoc[tok2]["gramm"].copy())
                        a = self.devoc[tok1]["gramm"].copy() + self.devoc[tok2]["gramm"].copy()
                        print(a)
                        print(a in self.gramms)
                        print(texts[i])
                        print(i)
                        new_gramms[tok1][tok2]["num"] += 1
            ngrams = []
            for key_1 in new_gramms.keys():
                for key_2 in new_gramms[key_1].keys():
                    ngrams.append((new_gramms[key_1][key_2]["num"], new_gramms[key_1][key_2]["gramm"]))
            ngrams = sorted(ngrams, reverse=True)
            return ngrams

        # ngrams = []
        # for gramm in tqdm(self.gramms):
        #    for gramm1 in self.gramms:
        #        curr_gramm = gramm.copy()
        #        curr_gramm_1 = gramm1.copy()
        #        curr_gramm = curr_gramm + curr_gramm_1
        #        if curr_gramm in self.gramms:
        #            pass
        #        else:
        #            curr_num = self.count_freq(curr_gramm, str_texts)
        #            ngrams.append((curr_num, curr_gramm))
        # ngrams = sorted(ngrams, reverse=True)

    def adopt_NG(self, gramm, num):
        """

        Add new gramm to self.vocab (with num)

        :param gramm: Current gramm
        :param num: The number of times this gramm has been encountered in the corpus

        :return: Nothing

        """

        curr_path = self.vocab
        if len(gramm) < 2:
            print(gramm)
            print("Фигня с граммой")
        else:

            i = 0
            last_token = self.last_token + 1
            while i < len(gramm):
                if gramm[i] in curr_path:
                    if i == (len(gramm) - 1):
                        if curr_path[gramm[i]]["empty"]:
                            token = self.giveNT()
                            curr_path[gramm[i]]["num"] = num
                            curr_path[gramm[i]]["token"] = token
                            curr_path[gramm[i]]["empty"] = False
                            self.gramms.append(gramm)
                            self.devoc[token] = {"num": num, "gramm": gramm}
                    else:
                        last_token = curr_path[gramm[i]]["token"]
                        curr_path = curr_path[gramm[i]]["vocab"]
                else:
                    if i == (len(gramm) - 1):
                        token = self.giveNT()
                        curr_voc = {"num": num, "token": token, "vocab": {}, "empty": False}
                        curr_path[gramm[i]] = curr_voc
                        self.gramms.append(gramm)
                        self.devoc[token] = {"num": num, "gramm": gramm}
                    else:
                        curr_voc = {"num": 0, "token": last_token, "vocab": {}, "empty": True}
                        curr_path[gramm[i]] = curr_voc
                        curr_path = curr_path[gramm[i]]["vocab"]
                i += 1

    def count_freq(self, gramm, str_texts):
        """

        Count frequencies of current gramm

        :param gramm: Current gramm
        :param str_texts: Corpus of sequences

        :return: The number of times this gramm has been encountered in the corpus

        """
        num = 0
        curr_gramm = gramm.copy()
        curr_gramm = ",".join(np.array(curr_gramm).astype(str))
        for text in str_texts:
            num += text.count(curr_gramm)

        return num

    def tokenize(self, text, make_drop=False, prob=0.001):
        """

        Tokenize corpus of sequences

        :param text: Corpus of sequences, that we want to tokenize
        :param make_drop: If true, than piece of the sequence can be encoded by the
                     simplest elements - quants with some probability ("prob")
        :param prob: The probability that a given piece of the sequence will be encoded by the
                     simplest elements - quants

        :return: Array with tokenized sequences

        """
        ind = 0
        res_mass = [self.start_token]
        if len(text) > 0:

            curr_voc = self.vocab[text[0]]
            forw_ind = ind
            forw_voc = curr_voc
            in_empty = False
            while ind + 1 < len(text):
                if in_empty:
                    if forw_ind + 2 == len(text):
                        if text[forw_ind + 1] in forw_voc["vocab"]:
                            if forw_voc["vocab"][text[forw_ind + 1]]["empty"]:
                                in_empty = False
                                curr_token = int(curr_voc["token"])
                                if curr_voc["empty"]:
                                    print("Добавляем проблемный токен")
                                res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                                # res_mass.append(curr_token)
                                curr_voc = self.vocab[text[ind + 1]]
                                ind += 1
                            else:
                                curr_token = int(forw_voc["vocab"][text[forw_ind + 1]]["token"])
                                res_mass.append(curr_token)
                                curr_voc = self.vocab[text[forw_ind + 1]]
                                ind = forw_ind + 1
                        else:
                            in_empty = False
                            curr_token = int(curr_voc["token"])
                            if curr_voc["empty"]:
                                print("Добавляем проблемный токен")
                            res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                            curr_voc = self.vocab[text[ind + 1]]
                            ind += 1
                    else:
                        if text[forw_ind + 1] in forw_voc["vocab"]:
                            if forw_voc["vocab"][text[forw_ind + 1]]["empty"]:
                                forw_voc = forw_voc["vocab"][text[forw_ind + 1]]
                                forw_ind += 1
                            else:
                                curr_voc = forw_voc["vocab"][text[forw_ind + 1]]
                                ind = forw_ind + 1
                                in_empty = False
                        else:
                            in_empty = False
                            curr_token = int(curr_voc["token"])
                            if curr_voc["empty"]:
                                print("Добавляем проблемный токен")
                            res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                            curr_voc = self.vocab[text[ind + 1]]
                            ind += 1
                            if ind + 1 == len(text):
                                curr_token = int(curr_voc["token"])
                                if curr_voc["empty"]:
                                    print("Добавляем проблемный токен")
                                res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                else:
                    if text[ind + 1] in curr_voc["vocab"]:
                        if curr_voc["vocab"][text[ind + 1]]["empty"]:
                            if ind + 2 == len(text):
                                curr_token = int(curr_voc["token"])
                                if curr_voc["empty"]:
                                    print("Добавляем проблемный токен")
                                res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                                # res_mass.append(curr_token)
                                curr_voc = self.vocab[text[ind + 1]]
                                ind += 1
                                curr_token = int(curr_voc["token"])
                                if curr_voc["empty"]:
                                    print("Добавляем проблемный токен")
                                res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                                # res_mass.append(curr_token)
                            else:

                                in_empty = True
                                forw_voc = curr_voc["vocab"][text[ind + 1]]
                                forw_ind = ind + 1
                        else:
                            if ind + 2 == len(text):
                                curr_voc = curr_voc["vocab"][text[ind + 1]]
                                ind += 1
                                curr_token = int(curr_voc["token"])
                                if curr_voc["empty"]:
                                    print("Добавляем проблемный токен")
                                res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                                # res_mass.append(curr_token)
                            else:
                                curr_voc = curr_voc["vocab"][text[ind + 1]]
                                ind += 1

                    else:
                        if ind + 2 == len(text):
                            curr_token = int(curr_voc["token"])
                            if curr_voc["empty"]:
                                print("Добавляем проблемный токен")
                            res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                            curr_voc = self.vocab[text[ind + 1]]
                            ind += 1
                            curr_token = int(curr_voc["token"])
                            if curr_voc["empty"]:
                                print("Добавляем проблемный токен")
                            res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                        else:
                            curr_token = int(curr_voc["token"])
                            if curr_voc["empty"]:
                                print("Добавляем проблемный токен")
                            res_mass = self.correct_add(res_mass.copy(), curr_token, make_drop, prob)
                            # res_mass.append(curr_token)
                            curr_voc = self.vocab[text[ind + 1]]
                            ind += 1

        res_mass.append(self.end_token)
        return res_mass

    def correct_add(self, curr_mass, new_token, make_drop, prob):
        """

        Tokenize and add new element of current sequence to tokenized massive

        :param curr_mass: Massive with already tokenized elements
        :param new_token: New token which will be tokenized
        :param make_drop: If true, than this piece of the sequence can be encoded by the
                     simplest elements - quants with some probability ("prob")
        :param prob: The probability that a this piece of the sequence will be encoded by the
                     simplest elements - quants
        :return: Modified curr_mass
        """
        if make_drop:
            curr_prob = random.random()
            if curr_prob < prob:
                gramm = self.devoc[new_token]["gramm"]
                for ind in gramm:
                    curr_mass.append(self.vocab[ind]["token"])
                return curr_mass.copy()
            else:
                curr_mass.append(new_token)
                return curr_mass.copy()
        else:
            curr_mass.append(new_token)
            return curr_mass.copy()

    def detokenize(self, text, string=False):
        """

        Detokenize one sequence

        :param text: Tokenized sequence, that we want to detokenize
        :param string: If true than will return string detokenized sequence, if false - than array

        :return: Detokenized sequence

        """
        res_mass = []
        text = text[1:-1]
        for i in range(len(text)):
            res_mass = res_mass + self.devoc[text[i]]["gramm"]
        if string:
            return " ".join(np.array(res_mass).astype("str"))
        else:
            return np.array(res_mass)

    def sorted_devoc(self, num_print=-1):
        """

        Print sorted self.devoc

        :param num_print: Number of most frequently occurring gramms, that will be output

        :return: Sorted self.devoc

        """
        d1 = []
        if num_print == -1:
            num_print = len(self.devoc)
        for key in self.devoc.keys():
            d1.append([self.devoc[key]["num"], key, self.devoc[key]["gramm"]])
        d1 = sorted(d1, reverse=True)
        for i in range(min(len(d1), num_print)):
            print("token: " + str(d1[i][1]) + " num: " + str(d1[i][0]) + " gramm: " + str(d1[i][2]))
        return d1

    def save(self, foldername):
        """

        Save current tokenizer to folder (it must exist)

        :param foldername: Name of folder, where we will save tokenizer

        :return: Nothing

        """

        with open(foldername + '/vocab.pickle', 'wb') as handle:
            pickle.dump(self.vocab, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(foldername + '/devoc.pickle', 'wb') as handle:
            pickle.dump(self.devoc, handle, protocol=pickle.HIGHEST_PROTOCOL)

        file = open(foldername + '/info.txt', "w")
        if self.last_token != self.vocab_size:
            print("self.last_token!=self.vocab_size")
        file.write(str(self.last_token))
        file.close()

        with open(foldername + '/startvoc.txt', "wb") as fp:  # Pickling
            pickle.dump(self.start_voc, fp)

        with open(foldername + '/gramms.txt', "wb") as fp:  # Pickling
            pickle.dump(self.gramms, fp)

    def load(self, foldername):
        """

        Load tokenizer from folder

        :param foldername: Name of folder from where we will load tokenizer

        :return: Nothing

        """
        with open(foldername + '/vocab.pickle', 'rb') as handle:
            self.vocab = pickle.load(handle)

        with open(foldername + '/devoc.pickle', 'rb') as handle:
            self.devoc = pickle.load(handle)

        file = open(foldername + '/info.txt', "r")
        self.last_token = int(float(file.readline()))
        self.vocab_size = self.last_token
        file.close()

        with open(foldername + '/startvoc.txt', "rb") as fp:  # Unpickling
            self.start_voc = pickle.load(fp)

        with open(foldername + '/gramms.txt', "rb") as fp:  # Unpickling
            self.gramms = pickle.load(fp)



