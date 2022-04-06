#import pickle5 as pickle
import pickle

class LangConverter():
    """

    This class is made to convert texts to integer sequences (pipeline to MultigrammTokenizer)

    field totok: Dictionary which matches symbols with numbers
    field detok: Dictionary which matches numbers with symbols
    field last_ind: Current size of vocab

    method init: Just initalise
    method adopt: Make totok and detok, using set of letters
    method convert: Convert text with symbols to sequence
    method deconvert: Deconvert sequence to text
    method print_top: Prints gramms converted to text
    method save:
    method load:


    """
    def __init__(self):
        self.totok = {}
        self.detok = {}
        self.last_ind = -1

    def adopt(self, vocab_set):
        """

        Make totok and detok, using set of letters

        :param vocab_set: set of letters

        :return: Nothing

        """
        mass = vocab_set.copy()
        mass = list(mass)
        for i in range(len(mass)):
            self.totok[mass[i]] = self.last_ind + 1
            self.detok[self.last_ind + 1] = mass[i]
            self.last_ind += 1

    def convert(self, text):
        """

        Convert text with symbols to sequence

        :param text: Text, to be converted to sequence

        :return: Converted sequence

        """
        curr_text = text
        curr_text = list(curr_text)
        curr_mass = []
        for i in range(len(curr_text)):
            if curr_text[i] in self.totok:
                curr_mass.append(self.totok[curr_text[i]])
        return curr_mass

    def deconvert(self, mass):
        """

        Deconvert sequence to text

        :param mass: Sequence, to be deconverted to text

        :return: Deconverted text

        """
        curr_mass = mass.copy()
        curr_text = []
        for i in range(len(curr_mass)):
            curr_text.append(self.detok[curr_mass[i]])
        curr_text = "".join(curr_text)
        return curr_text

    def print_top(self, print_mass):
        """

        Prints gramms converted to text

        :param print_mass: Massive of top gramms (in integers)

        :return: Nothing

        """
        for i in range(len(print_mass)):
            if print_mass[i][2] != [-1]:
                print("num: " + "%6d" % print_mass[i][0] + " gramm:  " +
                    self.deconvert(print_mass[i][2]))

    def save(self, foldername):
        """

        Save current converter to folder (it must exist)

        :param foldername: Name of folder, where we will save converter

        :return: Nothing

        """

        with open(foldername + '/totok.pickle', 'wb') as handle:
            pickle.dump(self.totok, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(foldername + '/detok.pickle', 'wb') as handle:
            pickle.dump(self.detok, handle, protocol=pickle.HIGHEST_PROTOCOL)

        file = open(foldername + '/conv_info.txt', "w")
        file.write(str(self.last_ind))
        file.close()

    def load(self, foldername):
        """

        Load tokenizer from folder

        :param foldername: Name of folder from where we will load converter

        :return: Nothing

        """
        with open(foldername + '/totok.pickle', 'rb') as handle:
            self.totok = pickle.load(handle)

        with open(foldername + '/detok.pickle', 'rb') as handle:
            self.detok = pickle.load(handle)

        file = open(foldername + '/conv_info.txt', "r")
        self.last_ind = int(float(file.readline()))
        file.close()
