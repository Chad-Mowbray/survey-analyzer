import io
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class PdfExtractor:

    def __init__(self, filename):
        self.filename = filename


    def extract_text_by_page(self):
        with open(self.filename, 'rb') as fh:
            for page in PDFPage.get_pages(fh, 
                                        caching=True,
                                        check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)
                
                text = fake_file_handle.getvalue()
                yield text
        
                # close open handles
                converter.close()
                fake_file_handle.close()
                
        
    def extract_text_to_file(self):
        questions = [
            "How has remote instruction affected your experience in this class?",
            "%What is working, what is not working, in this class?"
        ]

        for page in self.extract_text_by_page():
            no_comment = page[8:]
            with open("output/complete_survey.txt", "a") as survey:
                survey.write(no_comment + "\n")


            # if re.search(questions[1], no_comment):
            #     print("yes")

           
            # self.write_question_file("output/complete_survey.txt")


    def write_individual_question_files(self):   # try using [file].seek(n) to get rid of initial junk

        with open("output/complete_survey.txt", 'r') as survey:
            whole = survey.read()
            # print(whole)
            first_question, second_question = whole.split("%What is working, what is not working, in this class?")

            with open("output/What_is_working.txt", "w") as working:
                working.write(second_question)

            with open("output/How_has_remote_instruction_affected_your_experience.txt", "w") as experience:
                experience.write(first_question)

        
        
