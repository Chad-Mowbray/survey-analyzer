import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('punkt')


class Formatter:

    def __init__(self, filename):
        self.filename = filename
        self.get_comments_by_student()


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
                    builder = ''
                    for match in iterator:
                        i = match.span()[1]
                        print(line[prev:i - 1])
                        comments.append(line[prev:i - 1])
                        # builder += line[prev:i - 1] + " "
                        prev = i -1
                    # comments.append(builder)
                    # builder = ''
                    print("################")
                else:
                    comments.append(line)

        self.comments_by_student = comments


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

        self.clean_and_stemmed_comments = clean_and_stemmed
