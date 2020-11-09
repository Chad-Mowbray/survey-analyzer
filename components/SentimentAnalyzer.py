import re
from nltk.sentiment import SentimentAnalyzer
from textblob import TextBlob

# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')


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

        # intensity_analyzer = SentimentIntensityAnalyzer()
        for s in self.data:
            textblob_analyzer = TextBlob(s)
            textblob_combined = round(textblob_analyzer.sentiment.polarity, 2)

            # intensity_analyzer_scores_pos, intensity_analyzer_scores_neg = intensity_analyzer.polarity_scores(s)['pos'], intensity_analyzer.polarity_scores(s)['neg']
            # intensity_analyzer_combined = round(intensity_analyzer_scores_neg + intensity_analyzer_scores_neg, 2)

            
            pol = textblob_combined
            # print("textblob score: ", textblob_combined)
            # print("intensity analyzer score: ", intensity_analyzer_combined)
            # print(s)
            # print()

            # if -0.1 <= pol <= 0.1:
            supplement = self.supplemental_check(s, pol)
            pol = round(pol + supplement, 2)
            
            pol = self.stock_phrases(s, pol)

            if pol not in individual_scores: individual_scores[pol] = 1
            else: individual_scores[pol] += 1


            total += pol
            num += 1

            if 0.5 <= pol <= 5: 
                sentiment_buckets["very_positive"] += 1
                with open("output/samples/veryPositiveExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif 0.09 <= pol <= 0.5: 
                sentiment_buckets["somewhat_positive"] += 1
                with open("output/samples/somewhatPositiveExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif -0.09 <= pol <= 0.09: 
                if pol == 0: print(s)
                sentiment_buckets["neutral"] += 1
                with open("output/samples/neutralExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif -0.5 <= pol <= -0.09: 
                sentiment_buckets["somewhat_negative"] += 1
                with open("output/samples/somewhatNegativeExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")
            elif -5 <= pol <= -0.5: 
                sentiment_buckets["very_negative"] += 1
                with open("output/samples/veryNegativeExamples.txt", 'a') as file: file.write(str(pol) + " " + s + "\n")


        self.sentiment_buckets = sentiment_buckets
        self.average_sentiment = round(total / num, 2)

        sorted_dict = {}
        ordered_scores = sorted(individual_scores.keys())
        for s in ordered_scores:
            sorted_dict[s] = individual_scores[s]

        self.individual_scores = sorted_dict

        self.three_buckets = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        for score in self.individual_scores:
            if float(score) < -.07:
                self.three_buckets["negative"] += self.individual_scores[score]
            elif float(score) < .07:
                self.three_buckets["neutral"] += self.individual_scores[score]
            elif float(score) < 5:
                self.three_buckets["positive"] += self.individual_scores[score]
        # print()          
        # print(self.three_buckets)



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


        ## negative: challenge, struggle, distant, disconnected, miss, [less confident|connected], strange, weird
        ## neutral: [hasn't affected]

        if re.search(negative_words, comment, re.IGNORECASE):
            # print("Subtracting .15")
            if re.search(adjectives, comment[:re.search(negative_words, comment, re.IGNORECASE).span()[0]]):
                # print("# Subracting .25")
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
            print("@@@@@@@@@@@@@@", comment)
            return 0
        else: 
            return pol