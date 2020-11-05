from components.PdfExtractor import PdfExtractor
from components.Formatter import Formatter
from components.SentimentAnalyzer import SentimentAnalyzer



if __name__ == "__main__":
    extractor = PdfExtractor("input/evals.pdf")
    extractor.extract_text_to_file()
    extractor.write_individual_question_files()

    remote_instruction_formatter = Formatter("output/How_has_remote_instruction_affected_your_experience.txt")
    data = remote_instruction_formatter.comments_by_student
    for c in data:
        print(c)
    # print(data)

    # SentimentAnalyzer

