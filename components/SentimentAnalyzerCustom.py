import nltk
import random
import pickle
from nltk.tokenize import word_tokenize, RegexpTokenizer
# from training_data.data import pos, neg, neut
from training_data.data import pos, neg, neut
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('punkt')



class SentimentAnalyzerCustom:

    def __init__(self):
        print("initialized...")
        self.data = (
                    [(p, 'positive') for p in pos]+
                    [(n, 'negative') for n in neg]+
                    [(n, 'neutral') for n in neut]
                    )
        self.cleaned_data = None
        self.stopwords = set(stopwords.words('english')) 
        self.stemmer = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.cleaned_tokens = None
        self.model = None


    def prepare_training_data(self):
        new_data = []
        for comment in self.data:
            # print(category)
            rebuilt_comment = []
            for token in self.tokenizer.tokenize(comment[0].lower()):
                # print(token)
                
                if token not in self.stopwords:
                    clean_token = self.stemmer.stem(token)
                    # print(clean_token)
                    rebuilt_comment.append(clean_token)
                
            new_data.append( (" ".join(rebuilt_comment), comment[1] ) )

        self.cleaned_data = new_data
        # print(new_data)

        # tokens = set(word.lower() for words in self.cleaned_data for word in word_tokenize(words[0]))
        tokens = set(word.lower() for words in self.cleaned_data for word in self.tokenizer.tokenize(words[0]))

        print("total tokens: ", len(tokens))
        self.cleaned_tokens = tokens



    # # create an array of tuples (obj, classification)
    # # add all the tokens as keys to the object
    def create_train_feature_set(self):
        train = []

        for comment in self.data:
            item_dict = {}
            for token in self.cleaned_tokens:
                # item_dict[token] = token in word_tokenize(comment[0])
                item_dict[token] = token in self.tokenizer.tokenize(comment[0])

                # print(item_dict)
            item_dict["length"] = len(comment)
            train.append( (item_dict, comment[1]) )
            del item_dict

        self.train_feature_set = train
        # print(self.train_feature_set)


    def train(self):
        random.shuffle(self.train_feature_set)
        print(len(self.train_feature_set))
        train_x=self.train_feature_set[0:110]
        test_x=self.train_feature_set[110:123]

        model = nltk.NaiveBayesClassifier.train(train_x)
        self.model = model
        acc = nltk.classify.accuracy(model, test_x)
        print("Accuracy:", acc)

        model.show_most_informative_features()
        self.preserve(acc)


    def preserve(self, accuracy):
        self.pickle_file = f"training_data/NBC-{accuracy}.pickle"
        with open(self.pickle_file, "wb") as model_file:
            pickle.dump(self.model, model_file)


    def test(self, test_data):
        # test_data = neut

        # stemmer = PorterStemmer()
        # tokenizer = RegexpTokenizer(r'\w+')
        new_tests = []
        for comment in test_data:
            # print(category)
            rebuilt_comment = []
            for token in self.tokenizer.tokenize(comment.lower()):
                # print(token)
                
                if token not in self.stopwords:
                    clean_token = self.stemmer.stem(token)
                    # print(clean_token)
                    rebuilt_comment.append(clean_token)
                
            new_tests.append( " ".join(rebuilt_comment) )

        # print(new_tests)

        for test in new_tests:
            # t_features = {word: (word in word_tokenize(test.lower())) for word in self.cleaned_tokens}
            t_features = {word: (word in self.tokenizer.tokenize(test.lower())) for word in self.cleaned_tokens}

            print(test," : ", self.model.classify(t_features)) 
            # print(t_features)
            prob_dist = self.model.prob_classify(t_features)
            print("pos: ", prob_dist.prob("positive"), "neg: ", prob_dist.prob("negative"), "neut: ", prob_dist.prob("neutral"))
            print()


        # for test in neut:
        #     t_features = {word: (word in word_tokenize(test.lower())) for word in self.cleaned_tokens}
        #     print(test," : ", self.model.classify(t_features)) 


if __name__ == "__main__":
    x = SentimentAnalyzerCustom()
    x.prepare_training_data()
    x.create_train_feature_set()
    x.train()
    x.test()