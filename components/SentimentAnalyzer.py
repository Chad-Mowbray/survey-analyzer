from nltk.sentiment import SentimentAnalyzer
from textblob import TextBlob


class SentimentAnalyzer:

    def __init__(self, data):
        self.data = data
        self.get_sentiment_analysis()


    def get_sentiment_analysis(self):

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
            pol = feel.sentiment.polarity
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


        # print(sentiment_buckets)
        # print("Overall Average: ", total / num)
        self.sentiment_buckets = sentiment_buckets
        self.average_sentiment = total / num
