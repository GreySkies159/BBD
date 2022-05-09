import pdfplumber
from tkinter import ttk
import re


def get_filtered_text(file_to_parse: str):
    full_text = ''
    filtered_text = ''
    font_size = get_most_common_size_from_file(file_to_parse)
    if_abstract = 0

    # references
    references_found = 0
    references_list = ''

    with pdfplumber.open(file_to_parse) as pdf:
        # print(pdf.pages)
        for i in range(len(pdf.pages)):
            page_text = pdf.pages[i].dedupe_chars(tolerance=1)

            if i == 0 or i == 1 or i == 2:
                if if_abstract == 0:
                    #print(page_text.extract_text())
                    if_abstract = abstract_of_page(page_text.extract_text())

            filtered_text = page_text.filter(
                lambda obj: (obj["object_type"] == "char" and round(obj["size"], 0) > font_size)
                            or (
                                    ('Bold' in str(obj.get('fontname')) or
                                     'bold' in str(obj.get('fontname')))
                                    and round(obj["size"], 0) >= font_size))

            if i > len(pdf.pages) / 2:
                if references_found == 1:
                    references_list = references_list + page_text.extract_text().lower()
                if "references" in filtered_text.extract_text().lower():
                    references_found = 1
                    references_list = page_text.extract_text().lower()

            full_text = full_text + filtered_text.extract_text()
        print(references_list)
        references_number = re.findall('[\[]\d+[\]]', references_list)
        print(references_number)
        max_reference = 0
        for number in references_number:
            number = number[1:-1]
            int_number = int(number)
            if int_number > max_reference:
                max_reference = int_number
            print(max_reference)
            page_text.close()


    return full_text, max_reference, if_abstract


def get_most_common_size_from_file(pdf_file):
    font_size_dictionary = {}
    most_occurent_size_times = 0
    with pdfplumber.open(pdf_file) as pdf:
        for i in range(len(pdf.pages)):
            text = pdf.pages[i]
            for character in range(len(text.chars)):
                # if text.chars[character].get('object_type') == 'char':
                if text.chars[character].get('text') != ' ':
                    # TODO trunc size to be int
                    text_size = round(text.chars[character].get('size'), 0)
                    # TODO temp output
                    # text_font = text.chars[character].get('fontname')
                    # if("bold" in text_font or "Bold" in text_font):
                    # print(text_font)
                    # if theres no value for this size
                    if text_size not in font_size_dictionary.keys():
                        font_size_dictionary[text_size] = 1
                    if text_size in font_size_dictionary:
                        font_size_dictionary[text_size] += 1
                        if font_size_dictionary[text_size] > most_occurent_size_times:
                            most_occurent_size_times = font_size_dictionary[text_size]
        # print(font_size_dictionary)
        # print(most_occurent_size_times)
        most_common_size = [k for k, v in font_size_dictionary.items() if v == most_occurent_size_times]
        # print(most_common_size)
    return most_common_size[0]


def structure_evaluation(file_to_parse: str) -> int:
    #get filtered text
    filtered_text, max_reference_number, if_abstract = get_filtered_text(file_to_parse)
    filtered_text = filtered_text.lower()

    #checkbox value declaration
    abstract = 0
    introduction = 0
    methods = 0
    conclusion = 0
    references = 0
    extra_structure = 0


    introduction_index = 0
    conclusion_index = 0
    references_index = 0

    if if_abstract == 1:
        #print("Abstract found")
        abstract = 1
    elif 'abstract' in filtered_text:
        #print("abstract found")
        abstract = 1


    if 'introduction' in filtered_text:
        introduction_index = filtered_text.find('introduction')
        #print("Introduction found")
        introduction = 1
    if 'conclusion' in filtered_text:
        conclusion_index = filtered_text.find('conclusion')
        #print("Conclusion found")
        conclusion = 1
    if 'references' in filtered_text:
        references_index = filtered_text.find('references')
        #print("References found")
        references = 1

    if introduction_index != -1 and (conclusion_index != -1 or references_index != -1):
        if conclusion_index - introduction_index > 0 or references_index - introduction_index > 0:
            #print("Methods found")
            methods = 1

    if 'acknowledgments' in filtered_text or 'discussion' in filtered_text or  'future works' in filtered_text :
        extra_structure = 1

    return abstract, introduction, methods, conclusion, references, extra_structure, max_reference_number



def abstract_of_page(page_text: str):
    abstract = 0
    page_text = page_text.lower()
    '''
    used for structure analysis on first few pages
    :return:
    '''
    if 'abstract' in page_text:
        abstract = 1
        return abstract
