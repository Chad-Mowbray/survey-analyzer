import re
from textblob import TextBlob

import nltk
import pickle
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.porter import PorterStemmer
nltk.download("punkt")


class SentimentAnalyzer:

    def __init__(self, data, pickle_file):
        self.data = data
        self.supplemental_model = None
        self.cleaned_tokens = None
        self.get_supplemental_model(pickle_file)
        self.stemmer = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.get_sentiment_analysis()
        

    def get_supplemental_model(self, pickle_file):
        with open(pickle_file, "rb") as pickled_model:
            model = pickle.load(pickled_model)
            self.supplemental_model = model
        
        with open("components/analyzers/custom_model/cleaned_tokens.pickle", "rb") as token_file:
            tokens = pickle.load(token_file)
            self.cleaned_tokens = tokens


    def get_sentiment_analysis(self):

        individual_scores = {}

        sentiment_buckets = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        comments_and_ratings = {
            "positive": [],
            "neutral": [],
            "negative": []
        }

        total = 0
        num = 0

        for s in self.data:
            textblob_analyzer = TextBlob(s)
            textblob_combined = round(textblob_analyzer.sentiment.polarity, 2)
            
            pol = textblob_combined

            supplement = self.supplemental_check(s, pol)
            pol = round(pol + supplement, 2)
            
            pol = self.stock_phrases(s, pol)

            if pol not in individual_scores: individual_scores[pol] = 1
            else: individual_scores[pol] += 1

            total += pol
            num += 1

            if pol < -.07: 
                sentiment_buckets["negative"] += 1
                comments_and_ratings["negative"].append( ("negative", s) )
                with open("output/samples/negativeExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif pol < .07: 
                sentiment_buckets["neutral"] += 1
                comments_and_ratings["neutral"].append( ("neutral", s) )
                with open("output/samples/neutralExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif pol < 5: 
                sentiment_buckets["positive"] += 1
                comments_and_ratings["positive"].append( ("positive", s) )
                with open("output/samples/positiveExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")


        self.sentiment_buckets = sentiment_buckets
        self.average_sentiment = round(total / num, 2)

        sorted_dict = {}
        ordered_scores = sorted(individual_scores.keys())
        for s in ordered_scores:
            sorted_dict[s] = individual_scores[s]

        self.individual_scores = sorted_dict

        self.comments_and_ratings = comments_and_ratings



    def supplemental_check(self, comment, pol):
        total = pol
        well = "well"
        negative_words = "diffic"
        adjectives = "[\bvery|\bmore|\bmany|\bextremely]"
        hard = "[\bhard|\bchallenge|\bstruggle|\bless|\bchallenging][\bharder]"
        challenge = "[\bdistant|\bdisconnected|\bmiss]"
        strange = "[\bstrange|\bweird]"
        no_effect = "[\bhasn't affected]"
        positive = "positive"


        if re.search(negative_words, comment, re.IGNORECASE):
            if re.search(adjectives, comment[:re.search(negative_words, comment, re.IGNORECASE).span()[0]]):
                total -= .45
            else:
                total -= .2
        if re.search(hard, comment, re.IGNORECASE):
            total -= .3
        if re.search(challenge, comment, re.IGNORECASE):
            total -= .3
        if re.search(strange, comment, re.IGNORECASE):
            total -= .3
        if re.search(well, comment, re.IGNORECASE):
            total += .3
        if re.search(positive, comment, re.IGNORECASE):
            total += .2
        if re.search(no_effect, comment, re.IGNORECASE):
            total /= 4
        
        return total


    def stock_phrases(self, comment, pol):
        neutral_stock = [
            "No major problems have come up.", "No issues.", "No complaints.", "Unsure", "No", "Not sure.", "No effect",\
            "Not significantly", "No, it has not.", "No complaints", "Not at all", "Things are about the same.", "Not really that much.",\
            "Barely at all", "Nothing so far.", "It has not.", "No, it has not.", "Not at all", "No effect", "No complaints.", "It has not",\
            "Not much", "I don't think it has.", "Yes", "Very little", "Little", "None", "Not much."
            ]

        if comment in neutral_stock: 
            return 0
        else: 
            return pol