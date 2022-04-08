import pdfplumber
import math

def get_filtered_text(file_to_parse: str, font_size) -> str:
    full_text = ''
    filtered_text = ''
    with pdfplumber.open(file_to_parse) as pdf:
        for i in range(len(pdf.pages)):
            # TODO change to take all pages
            page_text = pdf.pages[i].dedupe_chars(tolerance=1)

            # TODO replace by seperate function
            filtered_text = page_text.filter(lambda obj: (obj["object_type"] == "char" and round(obj["size"],0) > font_size)
                                                         or (
                                                                ('Bold' in str(obj.get('fontname')) or
                                                                'bold' in str(obj.get('fontname')))
                                                                and obj["size"] >= font_size))

            # lambda obj: (obj["object_type"] == "char" and obj["size"] > font_size) or (('Bold' in obj["fontname"] or 'bold' in obj["fontname"]) and obj["size"] >= font_size))
            full_text = full_text + filtered_text.extract_text()

            page_text.close()

    print(full_text)
    print(type(full_text))
    return full_text


def get_most_common_size_from_file(pdf_file):
    font_size_dictionary = {}
    most_occurent_size_times = 0
    with pdfplumber.open(pdf_file) as pdf:
        for i in range(len(pdf.pages)):
            text = pdf.pages[i]
            for character in range(len(text.chars)):
                # if text.chars[character].get('object_type') == 'char':
                if text.chars[character].get('text') != ' ':
                    #TODO trunc size to be int
                    text_size = round(text.chars[character].get('size'), 0)
                    # TODO temp output
                    #text_font = text.chars[character].get('fontname')
                    #if("bold" in text_font or "Bold" in text_font):
                        #print(text_font)
                    # if theres no value for this size
                    if text_size not in font_size_dictionary.keys():
                        font_size_dictionary[text_size] = 1
                    if text_size in font_size_dictionary:
                        font_size_dictionary[text_size] += 1
                        if font_size_dictionary[text_size] > most_occurent_size_times:
                            most_occurent_size_times = font_size_dictionary[text_size]
        print(font_size_dictionary)
        print(most_occurent_size_times)
        most_common_size = [k for k, v in font_size_dictionary.items() if v == most_occurent_size_times]
        print(most_common_size)
    return most_common_size[0]


def structure_evaluation(filtered_text):
    '''
    :param filtered_text:
    :return: list of int values [introduction, methods, conclusion, references]
    '''
    # TODO check if this text contians:
    '''
        introduction
        [methods, ]
        [conclusion, concluding remarks]
        references
    '''

#pdf_file = "C:\\Users\eglus\PycharmProjects\BBD\A Survey on Deep Learning Algorithms, Techniques,and Applications.pdf"
# reads correctly
#pdf_file="C:/Users/eglus/Desktop/bbd/pdfReferences/1702.07800.pdf"
#works with trunc function
#pdf_file="C:/Users/eglus/Desktop/bbd/pdfReferences/acs.jcim.9b00266.pdf"
#reads weirdly but good enough
pdf_file="C:/Users/eglus/Desktop/bbd/pdfReferences/bbw068.pdf"
#works really well
#pdf_file="C:/Users/eglus/Desktop/bbd/pdfReferences/Methods Ecol Evol - 2019 - Christin - Applications for deep learning in ecology.pdf"
#kinda works
#pdf_file="C:/Users/eglus/Desktop/bbd/pdfReferences/Molecular Systems Biology - 2016 - Angermueller - Deep learning for computational biology.pdf"



common_size = get_most_common_size_from_file(pdf_file)
print(common_size)

get_filtered_text(pdf_file, common_size)
