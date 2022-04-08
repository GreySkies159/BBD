'''#
from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

#file= "C:\\Users\eglus\PycharmProjects\BBD\"
file="C:\\Users\eglus\PycharmProjects\BBD\A Survey on Deep Learning Algorithms, Techniques,and Applications.pdf"
#file="C:\\Users\eglus\PycharmProjects\BBD\DSM11_01.pdf"


output_string = StringIO()
with open(file, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)
print(output_string.getvalue().strip())


'''
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
from collections import Counter


def most_frequent_size(List):
    occurence = Counter(List)
    return occurence.most_common(1)[0][0]


PDF_file = "C:\\Users\eglus\PycharmProjects\BBD\A Survey on Deep Learning Algorithms, Techniques,and Applications.pdf"
#PDF_file ="C:\\Users\eglus\PycharmProjects\BBD\DSM11_01.pdf"

Extract_Data = []
font_sizes = []
for page_layout in extract_pages(PDF_file):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):
                        Font_size = character.size
                        #getting array of the font sizes in the file
                        font_sizes.append(Font_size)
                Extract_Data.append([Font_size, (element.get_text())])
#print(font_sizes)
most_frequent_font_size=most_frequent_size(font_sizes)
print(most_frequent_font_size)
print(Extract_Data)
