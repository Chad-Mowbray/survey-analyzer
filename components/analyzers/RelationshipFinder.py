import re
from scipy.stats import mannwhitneyu, chisquare, chi2_contingency, ttest_ind, ttest_rel


class RelationshipFinder:

    def __init__(self, comments_and_ratings, base_dist):
        self.comments_and_ratings = comments_and_ratings
        self.base_dist = base_dist

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
        
        # print("count in get_base_info: ", count)
        self.significance_test(count)
        print(f"{regex}: {percents}")
        return percents


    def significance_test(self, count_obj):

        print("count_obj: ", count_obj)
        print("base dist: ", self.base_dist)

        base_dist = []
        comparison = []

        for key in count_obj:
            if key == "positive":
                for i in range(count_obj[key]):
                    comparison.append("positive")
            elif key == "neutral":
                for i in range(count_obj[key]):
                    comparison.append("neutral")
            elif key == "negative":
                for i in range(count_obj[key]):
                    comparison.append("negative")
        
        for key in self.base_dist:
            if key == "positive":
                for i in range(count_obj[key]):
                    base_dist.append("positive")
            elif key == "neutral":
                for i in range(count_obj[key]):
                    base_dist.append("neutral")
            elif key == "negative":
                for i in range(count_obj[key]):
                    base_dist.append("negative")  

        # # print(comparison)      
        # u_statistic, p_value = mannwhitneyu(base_dist, comparison)
        # print("u_statistic: ", u_statistic, " p_value: ", p_value)

        # # print(self.base_dist.values(), count_obj.values())
        # combined = [list(self.base_dist.values()), list(count_obj.values())]
        # stat, p, dof, expected = chi2_contingency(combined)
        # print("chi p: ", p, p <= 0.05)

        # chisq, p = chisquare(list(self.base_dist.values()), list(count_obj.values()) )
        # print(" p: ", p)

        # stat, pval = ttest_ind(list(self.base_dist.values()), list(count_obj.values()))
        # print("ttest p: ", pval)

        # statxs, pvals = ttest_rel(list(self.base_dist.values()), list(count_obj.values()))
        # print("ttest rel p: ", pvals)
        # print()


        ## convert to relative number (based on the subsample)
        # base = [409, 305, 1331]
        # samp = [1,1,7]
        # samp = [2,3,14]
        # samp = [42,19,156]
        # samp = [4,3,14]
        # samp = [79, 55,227]
        # samp = [89, 53,222 ]
        # samp = [5,3,24]
        # percents = [0.2, 0.15, 0.65]

        # total = sum(samp)

        # new_base = []
        # for i in range(len(samp)):
        # new_base.append(percents[i] * total)

        # print(new_base)
        # chisq, p = chisquare(new_base, samp)
        # print(chisq, p)