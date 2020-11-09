from components.PdfExtractor import PdfExtractor
from components.Formatter import Formatter
from components.SentimentAnalyzer import SentimentAnalyzer
from components.plotters.SentimentPlotter import SentimentPlotter
from components.plotters.SentimentScatterPlot import SentimentScatterPlot

from components.RelationshipFinder import RelationshipFinder

from components.CategoryBigrams import CategoryBigrams

from components.plotters.OverlayPlotter import OverlayPlotter

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

    lab_regex = r"^lab" # maybe include science too
    lab_info = relationship.get_base_info(lab_regex)
    print("lab ratio: ", lab_info)

    lang_regex = "language"
    lang_info = relationship.get_base_info(lang_regex)
    print("language ratio: ", lang_info)

    discuss_regex = "discus"
    discuss_info = relationship.get_base_info(discuss_regex)
    print("discussion ratio: ", discuss_info)

    zoom_regex = "zoom"
    zoom_info = relationship.get_base_info(zoom_regex)
    print("zoom ratio: ", zoom_info)

    connection_regex = r"connect(?!.*internet)+(?=.*\b(?:students|peers|professor|everyone|classmates|people)\b)"
    connection_info = relationship.get_base_info(connection_regex)
    print("connection ratio: ", connection_info)

    lecture_regex = "lectur"
    lecture_info = relationship.get_base_info(lecture_regex)
    print("lecture ratio: ", lecture_info)


    # Plot base
    plotter = SentimentPlotter(categories, "Three buckets", "Category", False)
    plotter.plot()

    # Plot overlay relationships
    overlay = OverlayPlotter(percents, lab_info, "Labs")
    overlay.plot()

    overlay = OverlayPlotter(percents, lang_info, "Language")
    overlay.plot()

    overlay = OverlayPlotter(percents, discuss_info, "Discussion")
    overlay.plot()

    overlay = OverlayPlotter(percents, zoom_info, "Zoom")
    overlay.plot()

    overlay = OverlayPlotter(percents, connection_info, "Personal Connections")
    overlay.plot()

    overlay = OverlayPlotter(percents, lecture_info, "Lecture")
    overlay.plot()


    # # Bigrams
    # bigram = CategoryBigrams(comments_and_ratings)
    # print("POSITIVE: ", bigram.sorted_positive_bigrams[:20])
    # print("NEUTRAL: ", bigram.sorted_neutral_bigrams[:20])
    # print("NEGATIVE: ", bigram.sorted_negative_bigrams[:20])


    # plotter = SentimentPlotter(categories, "Three buckets", "Category", False)
    # plotter.plot()

    # scatter = SentimentScatterPlot(individual_scores, "Sentiment Based on Free Response Text", "Sentiment Score", False)
    # scatter.plot()
