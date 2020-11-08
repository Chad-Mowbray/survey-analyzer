import re
import pickle
# from nltk.sentiment import SentimentAnalyzer
from textblob import TextBlob

# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')


class SentimentAnalyzer:

    def __init__(self, data, pickle_file, supplemental_cleaned_tokens):
        self.data = data
        self.supplemental_model = self.get_supplemental_model(pickle_file)
        self.supplemental_cleaned_tokens = supplemental_cleaned_tokens
        self.get_sentiment_analysis()


    def get_supplemental_model(self, pickle_file):
        with open(pickle_file, "rb") as pickled_model:
            model = pickle.load(pickled_model)
            return model


    def get_sentiment_analysis(self):

        individual_scores = {}

        sentiment_buckets = {
        "very_negative": 0,
        "somewhat_negative": 0,
        "neutral": 0,
        "somewhat_positive": 0,
        "very_positive": 0
        }

        total = 0
        num = 0

        tokenizer = RegexpTokenizer(r'\w+')
        agree_count = 0
        disagree_count = 0
        # intensity_analyzer = SentimentIntensityAnalyzer()
        for i,s in enumerate(self.data):
            print()
            print("-------")
            print(s)

            t_features = {word: (word in tokenizer.tokenize(s.lower())) for word in self.supplemental_cleaned_tokens}
            supp = self.supplemental_model.classify(t_features)
            # print("Supplementary: ", supp)
            prob_dist = self.supplemental_model.prob_classify(t_features)
            # print("pos: ", prob_dist.prob("positive"), "neg: ", prob_dist.prob("negative"), "neut: ", prob_dist.prob("neutral"))


            textblob_analyzer = TextBlob(s)
            textblob_combined = round(textblob_analyzer.sentiment.polarity, 2)
            # print(textblob_combined)

            if supp == "positive" and textblob_combined > 0.1:
                print(f"number: {i}, agree positive, {textblob_combined}")
                agree_count += 1
            elif supp == "negative" and textblob_combined < 0.1:
                print(f"number: {i}, agree negative, {textblob_combined}")
                agree_count += 1
            elif supp == "neutral" and -0.1 <= textblob_combined <= 0.1:
                print(f"number: {i}, agree neutral, {textblob_combined}")
                agree_count += 1
            else:
                print(f"number: {i}, disagree, \nTextblob:{textblob_combined}, Custom:{supp}")
                disagree_count += 1

            # intensity_analyzer_scores_pos, intensity_analyzer_scores_neg = intensity_analyzer.polarity_scores(s)['pos'], intensity_analyzer.polarity_scores(s)['neg']
            # intensity_analyzer_combined = round(intensity_analyzer_scores_neg + intensity_analyzer_scores_neg, 2)

            
            pol = textblob_combined
            # print("textblob score: ", textblob_combined)
            # print("intensity analyzer score: ", intensity_analyzer_combined)
            # print(s)
            # print()

            if -0.1 <= pol <= 0.1:
                supplement = self.supplemental_check(s, pol)
                pol = round(pol + supplement, 2)
            
            pol = self.stock_phrases(s, pol)

            if pol not in individual_scores: individual_scores[pol] = 1
            else: individual_scores[pol] += 1


            total += pol
            num += 1

            if 0.5 <= pol <= 2: 
                sentiment_buckets["very_positive"] += 1
                with open("output/samples/veryPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif 0.1 <= pol <= 0.5: 
                sentiment_buckets["somewhat_positive"] += 1
                with open("output/samples/somewhatPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif -0.1 <= pol <= 0.1: 
                # if pol == 0: print(s)
                sentiment_buckets["neutral"] += 1
                with open("output/samples/neutralExamples.txt", 'a') as file: file.write(s + "\n")
            elif -0.5 <= pol <= -0.1: 
                sentiment_buckets["somewhat_negative"] += 1
                with open("output/samples/somewhatNegativeExamples.txt", 'a') as file: file.write(s + "\n")
            elif -2 <= pol <= -0.5: 
                sentiment_buckets["very_negative"] += 1
                with open("output/samples/veryNegativeExamples.txt", 'a') as file: file.write(s + "\n")

        print(f"agree: {agree_count}, disagree: {disagree_count}")
        self.sentiment_buckets = sentiment_buckets
        self.average_sentiment = round(total / num, 2)

        sorted_dict = {}
        ordered_scores = sorted(individual_scores.keys())
        for s in ordered_scores:
            sorted_dict[s] = individual_scores[s]

        self.individual_scores = sorted_dict


    def supplemental_check(self, comment, pol):
        negative_words = "diffic"
        adjectives = "[\bvery|\bmore|\bmany|\bextremely]"

        if re.search(negative_words, comment):
            # print("Subtracting .15")
            if re.search(adjectives, comment[:re.search(negative_words, comment).span()[0]]):
                # print("# Subracting .25")
                return pol - .45
            else:
                return pol - .2
        return pol


    def stock_phrases(self, comment, pol):
        neutral_stock = ["No major problems have come up.", "No issues.", "No complaints.", "Unsure", "No", "Not sure.", "No effect"]

        if comment in neutral_stock: return 0
        else: return pol