


class SentimentAnalyzer:

    def __init__(self, data):
        self.data = data

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
        for s in sentences:
            feel = TextBlob(s)
            pol = feel.sentiment.polarity
            total += pol
            num += 1
            # print(pol)
            # print(s)
            # print()
            if pol >= 0.4: 
                sentiment_buckets["very_positive"] += 1
                with open("sentimentExamples/veryPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= 0.1: 
                sentiment_buckets["somewhat_positive"] += 1
                with open("sentimentExamples/somewhatPositiveExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -0.1: 
                sentiment_buckets["neutral"] += 1
                with open("sentimentExamples/neutralExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -0.4: 
                sentiment_buckets["somewhat_negative"] += 1
                with open("sentimentExamples/somewhatNegativeExamples.txt", 'a') as file: file.write(s + "\n")
            elif pol >= -1: 
                sentiment_buckets["very_negative"] += 1
                with open("sentimentExamples/veryNegativeExamples.txt", 'a') as file: file.write(s + "\n")


        print(sentiment_buckets)
        print("Overall Average: ", total / num)
