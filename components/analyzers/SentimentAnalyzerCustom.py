import nltk
import random
from nltk.tokenize import word_tokenize, RegexpTokenizer
# from training_data.data import pos, neg, neut
from training_data.data import pos, neg, neut
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('punkt')



def SentimentAnalyzerCustom():

    stop_words = set(stopwords.words('english')) 

    data = (
        [(p, 'positive') for p in pos]+
        [(n, 'negative') for n in neg]
        )
        # [(n, 'neutral') for n in neut]

    stemmer = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    new_data = []
    for comment in data:
        # print(category)
        rebuilt_comment = []
        for token in tokenizer.tokenize(comment[0].lower()):
            # print(token)
            
            if token not in stop_words:
                clean_token = stemmer.stem(token)
                # print(clean_token)
                rebuilt_comment.append(clean_token)
            
        new_data.append( (" ".join(rebuilt_comment), comment[1] ) )

    print(new_data)



    tokens = set(word.lower() for words in data for word in word_tokenize(words[0]))
    print("total tokens: ", len(tokens))





    # # create an array of tuples (obj, classification)
    # # add all the tokens as keys to the object

    def create_train(tokens, data):
        train = []

        for comment in data:
            item_dict = {}
            for token in tokens:
                item_dict[token] = token in word_tokenize(comment[0])
                # print(item_dict)
            train.append( (item_dict, comment[1]) )
            del item_dict


        return train

    train = create_train(tokens, new_data)



    random.shuffle(train)
    print(len(train))
    train_x=train[0:45]
    test_x=train[45:52]

    model = nltk.NaiveBayesClassifier.train(train_x)
    acc=nltk.classify.accuracy(model, test_x)
    print("Accuracy:", acc)

    model.show_most_informative_features()



    # tests=['I really like it', 
    #     'I do not think this is good one', 
    #     'this is good one',
    #     'I hate the show!']

    for test in neut:
        t_features = {word: (word in word_tokenize(test.lower())) for word in tokens}
        print(test," : ", model.classify(t_features)) 


if __name__ =="__main__":
    SentimentAnalyzerCustom()