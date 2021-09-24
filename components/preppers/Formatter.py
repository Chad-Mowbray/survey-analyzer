import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('punkt')


class Formatter:

    def __init__(self, filename):
        self.filename = filename
        self.get_comments_by_student()


    def check_length(self, comments):
        return [c for c in comments if len(c) > 2]


    def get_comments_by_student(self):
        comments = []
        with open(self.filename, 'r') as file:
            for line in file.readlines():
                if line in ['', '\n']: continue

                pattern = '[\.?!,;:a-z]+[A-Z]+'
                if re.search(pattern, line):
                    p = re.compile(pattern)
                    iterator = p.finditer(line)
                    prev = 0
                    for match in iterator:
                        i = match.span()[1]
                        comments.append(line[prev:i - 1])
                        prev = i -1
                else:
                    comments.append(line)

        comments = self.check_length(comments)
        self.write_numbered_comments_file(comments, "RAW")
        self.comments_by_student = comments


    def write_numbered_comments_file(self, comments, detail):
        filename_base = self.filename.split("/")[1]
        with open(f"output/numbered_comments/{filename_base}-{detail}", "w") as numbered_file:
            for i,line in enumerate(comments):
                numbered_file.write(f"{i}:  {line}\n")


    def get_stemmed_comments_by_student(self):
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = set(stopwords.words('english'))

        clean_and_stemmed = []
        for comment in self.comments_by_student:
            rebuild_comment = []
            for token in tokenizer.tokenize(comment.lower()):
                if token not in stop_words:
                    clean_token = stemmer.stem(token)
                    rebuild_comment.append(clean_token)
            clean_and_stemmed.append(" ".join(rebuild_comment))

        clean_and_stemmed = self.check_length(clean_and_stemmed)
        self.write_numbered_comments_file(clean_and_stemmed, "STEMMED")
        self.clean_and_stemmed_comments = clean_and_stemmed
