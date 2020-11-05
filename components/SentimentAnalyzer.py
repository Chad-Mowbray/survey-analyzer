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
            if pol not in individual_scores: individual_scores[pol] = 1
            else: individual_scores[pol] += 1


            total += pol
            num += 1

            if pol >= 0.4: 
                sentiment_buckets["very_positive"] += 1
                with open("output/samples/veryPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= 0.1: 
                sentiment_buckets["somewhat_positive"] += 1
                with open("output/samples/somewhatPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -0.1: 
                sentiment_buckets["neutral"] += 1
                with open("output/samples/neutralExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -0.4: 
                sentiment_buckets["somewhat_negative"] += 1
                with open("output/samples/somewhatNegativeExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -1: 
                sentiment_buckets["very_negative"] += 1
                with open("output/samples/veryNegativeExamples.txt", 'a') as file: file.write(s + "\n")


        self.sentiment_buckets = sentiment_buckets
        self.average_sentiment = round(total / num, 2)

        sorted_dict = {}
        ordered_scores = sorted(individual_scores.keys())
        for s in ordered_scores:
            sorted_dict[s] = individual_scores[s]

        self.individual_scores = sorted_dict
