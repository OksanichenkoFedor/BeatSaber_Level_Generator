from FuncFiles.lang_converter import LangConverter
from FuncFiles.tokenizer import MultigrammTokenizer

class LangTokenizer:
    """

    This class is made to tokenize texts on dome language

    field converter: LangConverter of LangTokenizer
    field tokenizer: MultigrammTokenizer of LangTokenizer

    method init: Just initalise
    method adopt: Change vocabulary according to corpus of sequences, using some rules of evolution
    method tokenize: Tokenize corpus of text
    method detokenize: Detokenize one text
    method save: Save current LangTokenizer to folder (it must exist)
    method load: Load LangTokenizer from folder
    method print_top: Prints gramms, which are most often found

    """
    def __init__(self, vocab=None):
        if vocab is None:
            vocab = set([])
        if type(vocab) != type(set([])):
            print("Словарь не сет")

        self.converter = LangConverter()
        self.converter.adopt(vocab)
        self.tokenizer = MultigrammTokenizer(num=(self.converter.last_ind + 1))

    def adopt(self, texts, vocab_size=2000, ad_num=False, num_cycles=10, part_add=0.25,
              verbose_main=False, verbose_NGW=True):
        """

        Change vocabulary according to corpus of sequences, using some rules of evolution

        :param texts: Corpus of texts, on which we will make tokenizer
        :param vocab_size: Aim of vocab size
        :param ad_num: Boolean, if True, then adding new "words" will be repeated exact number of times (num)
                                if False, then adding will continue, while vocab is not filled
        :param num_cycles: Number of adding cycles
        :param part_add: Part of new gramms, which must be added in every "adopt_onse"
        :param verbose_main: If true, there will appear tqdm progress bar in main loop, if false - no
        :param verbose_NGW: If true, there will appear tqdm progress bar in every "adopt_once", if false - no

        :return: Nothing

        """
        ind_texts = []
        for curr_str in texts:
            ind_texts.append(self.converter.convert(curr_str))

        self.tokenizer.adopt(ind_texts, vocab_size=vocab_size, ad_num=ad_num, num_cycles=num_cycles, part_add=part_add,
                             verbose_main=verbose_main, verbose_NGW=verbose_NGW)

    def tokenize(self, text, make_drop=False, prob=0.001):
        """

        Tokenize corpus of text

        :param text: Corpus of text, that we want to tokenize
        :param make_drop: If true, than piece of text can be encoded by the
                     simplest elements - quants with some probability ("prob")
        :param prob: The probability that a given piece of text will be encoded by the
                     simplest elements - quants

        :return: Array with tokenized text

        """
        ind_text = self.converter.convert(text)
        return self.tokenizer.tokenize(ind_text, make_drop=make_drop, prob=prob)

    def detokenize(self, text):
        """

        Detokenize one text

        :param text: Tokenized text, that we want to detokenize

        :return: Detokenized text

        """
        ind_text = self.tokenizer.detokenize(text)
        return self.converter.deconvert(ind_text)

    def save(self, foldername):
        """

        Save current LangTokenizer to folder (it must exist)

        :param foldername: Name of folder, where we will save LangTokenizer

        :return: Nothing

        """
        self.converter.save(foldername)
        self.tokenizer.save(foldername)

    def load(self, foldername):
        """

        Load LangTokenizer from folder

        :param foldername: Name of folder from where we will load LangTokenizer

        :return: Nothing

        """
        self.converter.load(foldername)
        self.tokenizer = MultigrammTokenizer(num=(self.converter.last_ind + 1))
        self.tokenizer.load(foldername)

    def print_top(self, num_print=-1):
        """

        Prints gramms, which are most often found

        :param num_print: Number of most frequently occurring gramms, that will be output

        :return: Nothing

        """
        mass = self.tokenizer.sorted_devoc(num_print=num_print)
        self.converter.print_top(mass, num_print = num_print)