import re
from nltk.sentiment import SentimentAnalyzer
from textblob import TextBlob


class Formatter:

    def __init__(self, filename):
        self.filename = filename
        self.get_comments_by_student()


    def get_comments_by_student(self):
        sentences = []
        with open(self.filename, 'r') as file:
            for line in file.readlines():
                if line in ['', '\n']: continue

                pattern = '[\.a-z]+[A-Z]+'
                if re.search(pattern, line):
                    p = re.compile(pattern)
                    iterator = p.finditer(line)
                    prev = 0
                    for match in iterator:
                        i = match.span()[1]
                        sentences.append(line[prev:i - 1])
                        prev = i -1
                else:
                    sentences.append(line)

        self.comments_by_student = sentences