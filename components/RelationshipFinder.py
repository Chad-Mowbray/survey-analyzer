import re


class RelationshipFinder:

    def __init__(self, comments_and_ratings):
        self.comments_and_ratings = comments_and_ratings
        # self.comments_and_ratings_base_ratio = self.get_base_ratio()
        self.lab_ratio = None
        self.language_ratio = None
        self.discussion_ratio = None
        

    # def get_base_ratio(self):

        # total = sum([num for num in self.comments_and_ratings.values()])
        # print(total)
        # percents = []
        # for category in self.comments_and_ratings:
        #     percents.append(round(self.comments_and_ratings[category] / total),2)

        # return percents


    def find_lab_info(self):
        # print(self.comments_and_ratings)
        count = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        for rating in self.comments_and_ratings:
            for comment in self.comments_and_ratings[rating]:
                if re.search("lab", comment[1], re.IGNORECASE):
                    count[comment[0]] += 1

        self.lab_ratio = count

        total = sum([num for num in count.values()])
        print(total)
        percents = []
        for category in count:
            percents.append(round(count[category] / total,2))
        
        print(percents)

        



    def find_language_info(self):
        # print(self.comments_and_ratings)
        count = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        regex = "language"

        for rating in self.comments_and_ratings:
            for comment in self.comments_and_ratings[rating]:
                if re.search(regex, comment[1], re.IGNORECASE):
                    count[comment[0]] += 1

        self.language_ratio = count

        total = sum([num for num in count.values()])
        print(total)
        percents = []
        for category in count:
            percents.append(round(count[category] / total,2))
        
        print(percents)

    def find_discussion_info(self):
        # print(self.comments_and_ratings)
        count = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        regex = "discus"

        for rating in self.comments_and_ratings:
            for comment in self.comments_and_ratings[rating]:
                if re.search(regex, comment[1], re.IGNORECASE):
                    count[comment[0]] += 1

        self.discussion_ratio = count

        total = sum([num for num in count.values()])
        print(total)
        percents = []
        for category in count:
            percents.append(round(count[category] / total,2))
        
        print(percents)