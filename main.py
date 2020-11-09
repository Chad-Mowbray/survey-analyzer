from components.PdfExtractor import PdfExtractor
from components.Formatter import Formatter
from components.SentimentAnalyzer import SentimentAnalyzer
from components.plotters.SentimentPlotter import SentimentPlotter
from components.plotters.SentimentScatterPlot import SentimentScatterPlot

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
    three_buckets = analyzer.three_buckets
    print(average, categories, individual_scores, three_buckets)

#     # plot sentiment
    # plotter = SentimentPlotter(categories, "Sentiment Based on Free Response Text","Category", False)
    # plotter.plot()

    plotter = SentimentPlotter(three_buckets, "Three buckets", "Category", False)
    plotter.plot()

    scatter = SentimentScatterPlot(individual_scores, "Sentiment Based on Free Response Text", "Sentiment Score", False)
    scatter.plot()

#     # # custom Sentiment
#     # custom = SentimentAnalyzerCustom(data)
#     # custom.process()


# # from textblob import TextBlob


# # x ="It's made it somewhat difficult to have a good dynamic between the students and instructor in terms of questions. Electronic handwritten notes do not work as well as whiteboardor chalkboard."

# # b = TextBlob(x)
# # print(b.sentiment)