from nltk import FreqDist, bigrams


class CategoryBigrams:
    """
    A mixin to handle bigram processing
    """
    def __init__(self, data):
        self.positive_data = [d[1] for d in data["positive"]]
        self.neutral_data = [d[1] for d in data["neutral"]]
        self.negative_data = [d[1] for d in data["negative"]]
        self.get_all_bigrams()
        self.bigrams_fdist = None
        self.sorted_bigrams = None

    def get_all_bigrams(self):
        self.sorted_bigrams_positive = self.get_notes_bigrams(self.positive_data)
        self.sorted_bigrams_neutral = self.get_notes_bigrams(self.neutral_data)
        self.sorted_bigrams_negative = self.get_notes_bigrams(self.negative_data)

    
    def clean_data(self):
        


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