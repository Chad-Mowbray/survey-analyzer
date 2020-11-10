import re


class RelationshipFinder:

    def __init__(self, comments_and_ratings):
        self.comments_and_ratings = comments_and_ratings
        

    def get_base_info(self, regex):
        count = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        for rating in self.comments_and_ratings:
            for comment in self.comments_and_ratings[rating]:
                if re.search(regex, comment[1], re.IGNORECASE):
                    count[comment[0]] += 1
                    # print(comment)

        total = sum([num for num in count.values()])
        percents = []
        for category in count:
            percents.append(round(count[category] / total,2))
        
        print(f"{regex}: {percents}")
        return percents
