from components.preppers.PdfExtractor import PdfExtractor
from components.preppers.Formatter import Formatter
from components.analyzers.SentimentAnalyzer import SentimentAnalyzer
from components.plotters.SentimentPlotter import SentimentPlotter
from components.plotters.SentimentScatterPlot import SentimentScatterPlot
from components.analyzers.RelationshipFinder import RelationshipFinder
from components.analyzers.CategoryBigrams import CategoryBigrams
from components.plotters.OverlayPlotter import OverlayPlotter



def overlay_plot(percents, info):
    overlay = OverlayPlotter(percents, info[0], info[1])
    overlay.plot()


def plot_base(categories):
    plotter = SentimentPlotter(categories, "Sentiment Categorization by Comment", "Sentiment Category")
    plotter.plot()


def find_relationships(comments_and_ratings):
    relationship = RelationshipFinder(comments_and_ratings)

    lab_regex = r"^lab"
    lang_regex = "language"
    discuss_regex = "discus"
    zoom_regex = "zoom"
    connection_regex = r"connect(?!.*internet)+(?=.*\b(?:students|peers|professor|everyone|classmates|people)\b)"
    lecture_regex = "lectur"
    canvas_regex = "canvas"

    regex = ( (lab_regex, "Labs"), (lang_regex, "Foreign Language"), (zoom_regex, "Zoom"), (canvas_regex, "Canvas"), \
            (discuss_regex, "Discussion"), (lecture_regex, "Lecture"), (connection_regex, "Interpersonal Connections"))

    infos = []
    for r in regex:
        infos.append( (relationship.get_base_info(r[0]),r[1]) )
    
    return infos


def main():
    # extract text from pdf and separate each question
    extractor = PdfExtractor("input/evals.pdf")
    extractor.extract_text_to_file()
    extractor.write_individual_question_files()

    # format text so that comments are the units
    remote_instruction_formatter = Formatter("output/How_has_remote_instruction_affected_your_experience.txt")
    data = remote_instruction_formatter.comments_by_student

    # extract sentiment
    analyzer = SentimentAnalyzer(data, "components/analyzers/custom_model/NBC-0.9.pickle")
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
    plot_base(categories)

    infos = find_relationships(comments_and_ratings)
    [overlay_plot(percents,info) for info in infos] 


if __name__ == "__main__":
    main()
















    # Plot base
    # plotter = SentimentPlotter(categories, "Sentiment Categorization by Comment", "Sentiment Category")
    # plotter.plot()

    # Plot overlay relationships
    # overlay = OverlayPlotter(percents, lab_info, "Labs")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, lang_info, "Language")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, discuss_info, "Discussion")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, zoom_info, "Zoom")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, connection_info, "Personal Connections")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, lecture_info, "Lecture")
    # overlay.plot()

    # overlay = OverlayPlotter(percents, canvas_info, "Canvas")
    # overlay.plot()


    # # Bigrams
    # bigram = CategoryBigrams(comments_and_ratings)
    # print("POSITIVE: ", bigram.sorted_positive_bigrams[:20])
    # print("NEUTRAL: ", bigram.sorted_neutral_bigrams[:20])
    # print("NEGATIVE: ", bigram.sorted_negative_bigrams[:20])


    # plotter = SentimentPlotter(categories, "Three buckets", "Category", False)
    # plotter.plot()

    # scatter = SentimentScatterPlot(individual_scores, "Sentiment Based on Free Response Text", "Sentiment Score", False)
    # scatter.plot()
