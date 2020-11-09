from components.PdfExtractor import PdfExtractor
from components.Formatter import Formatter
from components.SentimentAnalyzer import SentimentAnalyzer
from components.plotters.SentimentPlotter import SentimentPlotter
from components.plotters.SentimentScatterPlot import SentimentScatterPlot

from components.RelationshipFinder import RelationshipFinder

# from components.SentimentAnalyzerCustom import SentimentAnalyzerCustom


if __name__ == "__main__":

    # extract text from pdf and separate each question
    extractor = PdfExtractor("input/evals.pdf")
    extractor.extract_text_to_file()
    extractor.write_individual_question_files()

    # format text so that comments are the units
    remote_instruction_formatter = Formatter("output/How_has_remote_instruction_affected_your_experience.txt")
    data = remote_instruction_formatter.comments_by_student

    # clean and stem words
    # remote_instruction_formatter.get_stemmed_comments_by_student()
    # data = remote_instruction_formatter.clean_and_stemmed_comments



    # extract sentiment
    # SentimentAnalyzer
    analyzer = SentimentAnalyzer(data)
    average = analyzer.average_sentiment
    categories = analyzer.sentiment_buckets
    individual_scores = analyzer.individual_scores
    comments_and_ratings = analyzer.comments_and_ratings
    print(average, categories, individual_scores)

    # get percent by category baseline
    total = sum([num for num in categories.values()])
    print(total)
    percents = []
    for category in categories:
        percents.append(round(categories[category] / total,2))
    print("BASE: ", percents)


    # Find relationships
    relationship = RelationshipFinder(comments_and_ratings)
    # print(relationship.comments_and_ratings_base_ratio )
    relationship.find_lab_info()
    print("lab ratio: ", relationship.lab_ratio)
    relationship.find_language_info()
    print("language ratio: ", relationship.language_ratio)
    relationship.find_discussion_info()
    print("discussion ratio: ", relationship.discussion_ratio)



    # plotter = SentimentPlotter(categories, "Three buckets", "Category", False)
    # plotter.plot()

    # scatter = SentimentScatterPlot(individual_scores, "Sentiment Based on Free Response Text", "Sentiment Score", False)
    # scatter.plot()
