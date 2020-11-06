import re
from nltk.sentiment import SentimentAnalyzer
from textblob import TextBlob


class SentimentAnalyzer:

    def __init__(self, data):
        self.data = data
        self.get_sentiment_analysis()


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

        for s in self.data:
            feel = TextBlob(s)
            pol = round(feel.sentiment.polarity, 2)
            # if pol == 0: print(s)

            if -0.1 <= pol <= 0.1:
                supplement = self.supplemental_check(s, pol)
                pol = round(pol + supplement, 2)

            if pol not in individual_scores: individual_scores[pol] = 1
            else: individual_scores[pol] += 1


            total += pol
            num += 1

            if 0.5 <= pol <= 1: 
                sentiment_buckets["very_positive"] += 1
                with open("output/samples/veryPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif 0.1 <= pol <= 0.5: 
                sentiment_buckets["somewhat_positive"] += 1
                with open("output/samples/somewhatPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif -0.1 <= pol <= 0.1: 
                if pol == 0: print(s)
                sentiment_buckets["neutral"] += 1
                with open("output/samples/neutralExamples.txt", 'a') as file: file.write(s + "\n")
            elif -0.5 <= pol <= -0.1: 
                sentiment_buckets["somewhat_negative"] += 1
                with open("output/samples/somewhatNegativeExamples.txt", 'a') as file: file.write(s + "\n")
            elif -1 <= pol <= -0.5: 
                sentiment_buckets["very_negative"] += 1
                with open("output/samples/veryNegativeExamples.txt", 'a') as file: file.write(s + "\n")


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