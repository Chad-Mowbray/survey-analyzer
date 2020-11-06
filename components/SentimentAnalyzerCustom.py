import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


class SentimentAnalyzerCustom:

    def __init__(self, data):
        self.data = data

    
    def process(self):
        analyzer = SentimentIntensityAnalyzer()
        for c in self.data:
            scores = analyzer.polarity_scores(c)

            print(scores)
            print(c)
            print()
