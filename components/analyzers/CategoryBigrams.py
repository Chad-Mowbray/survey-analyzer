import string

from nltk import FreqDist, bigrams
from nltk import download

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
download('stopwords')




class CategoryBigrams:

    def __init__(self, data):
        self.default_stopwords = stopwords.words('english')
        self.positive_data = [d[1] for d in data["positive"]]
        self.neutral_data = [d[1] for d in data["neutral"]]
        self.negative_data = [d[1] for d in data["negative"]]
        self.clean_all()
        # self.get_all_bigrams()
        # self.bigrams_fdist = None
        # self.sorted_bigrams = None

    # def get_all_bigrams(self):
    #     self.sorted_bigrams_positive = self.get_notes_bigrams(self.positive_data)
    #     self.sorted_bigrams_neutral = self.get_notes_bigrams(self.neutral_data)
    #     self.sorted_bigrams_negative = self.get_notes_bigrams(self.negative_data)

    def clean_all(self):
        positive_tokens = self.clean_data(self.positive_data)
        self.sorted_positive_bigrams = self.get_notes_bigrams(positive_tokens)

        neutral_tokens = self.clean_data(self.neutral_data)
        self.sorted_neutral_bigrams = self.get_notes_bigrams(neutral_tokens)

        negative_tokens = self.clean_data(self.negative_data)
        self.sorted_negative_bigrams = self.get_notes_bigrams(negative_tokens)

        # neutral_tokens = self.clean_data(self.neutral_data)
        # negative_tokens = self.clean_data(self.negative_data)
        # print(len(positive_tokens), len(neutral_tokens), len(negative_tokens))
    

    def clean_data(self, data):  #TODO: make tokens a set

        notes_stopwords = [n
                        if n not in self.default_stopwords
                        else ''
                        for note in data
                        for n in note.split(' ')]

        # make lowercase
        notes_lower = [n.lower() for n in notes_stopwords]

        # remove blanks
        notes_blanks = [n for n in notes_lower if len(n) > 0]

        # remove punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [n.translate(table) for n in notes_blanks]

        # remove non-alphabet characters
        notes_alpha = [n for n in stripped if n.isalpha()]

        # remove stopwords again
        notes_alpha2 = [n for n in notes_alpha if n not in self.default_stopwords]

        # print(notes_alpha2)
        return notes_alpha2




    @staticmethod
    def get_notes_bigrams(data):

        # run after self.clean
        bigrams_list = list(bigrams(data))
        bigrams_fdist = FreqDist(bigrams_list)
        bigram_freqs = []
        for k,v in bigrams_fdist.items():
            bigram_freqs.append((k,v))

        sorted_bigram_freqs = sorted(bigram_freqs, key=lambda x: x[1], reverse=True)

        temp_dict = {}
        for bigram in sorted_bigram_freqs:
            if bigram[0] in temp_dict:
                temp_dict[bigram[0]] += int(bigram[1])
            else:
                temp_dict[bigram[0]] = int(bigram[1])

        dict_copy = {}
        for key in temp_dict:
            if key not in dict_copy:
                dict_copy[key] = temp_dict[key]

            for k in temp_dict:
                if (k[1],k[0]) == key:
                    dict_copy[key] += temp_dict[(k[0],k[1])]
                    del dict_copy[key]

        mod_bigram_freqs = []
        for k,v in dict_copy.items():
            mod_bigram_freqs.append((k,v))

        mod_sorted_bigram_freqs = sorted(mod_bigram_freqs, key=lambda x: x[1], reverse=True)
        # self.sorted_bigrams = mod_sorted_bigram_freqs
        return mod_sorted_bigram_freqs