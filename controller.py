import pdfplumber


def get_filtered_text(file_to_parse: str):
    full_text = ''
    filtered_text = ''
    font_size = get_most_common_size_from_file(file_to_parse)
    if_abstract = 0

    with pdfplumber.open(file_to_parse) as pdf:
        #print(pdf.pages)
        for i in range(len(pdf.pages)):
            page_text = pdf.pages[i].dedupe_chars(tolerance=1)

            if i == 0 or i == 1 or i == 2:
                if if_abstract == 0:
                    print(page_text.extract_text())
                    if_abstract = abstract_of_page(page_text.extract_text())

            # TODO replace by seperate function
            filtered_text = page_text.filter(
                lambda obj: (obj["object_type"] == "char" and round(obj["size"], 0) > font_size)
                            or (
                                    ('Bold' in str(obj.get('fontname')) or
                                     'bold' in str(obj.get('fontname')))
                                    and obj["size"] >= font_size))

            # lambda obj: (obj["object_type"] == "char" and obj["size"] > font_size) or (('Bold' in obj["fontname"] or 'bold' in obj["fontname"]) and obj["size"] >= font_size))
            full_text = full_text + filtered_text.extract_text()

            page_text.close()

    # print(full_text)
    # print(type(full_text))
    return full_text, if_abstract


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


def structure_evaluation(filtered_text: str, abstract_score):
    '''
    :param filtered_text:
    :return:
    '''
    filtered_text = filtered_text.lower()
    structure_score = 0
    optional_structure_score = 0
    introduction_index = 0
    conclusion_index = 0
    references_index = 0

    if abstract_score == 1:
        structure_score = structure_score +1
        print("Abstract found")
    elif 'abstract' in filtered_text:
        structure_score = structure_score + 1
        print("abstract found")
    if 'introduction' in filtered_text:
        introduction_index = filtered_text.find('introduction')
        structure_score = structure_score + 1
        print("Introduction found")
    if 'conclusion' in filtered_text:
        conclusion_index = filtered_text.find('conclusion')
        structure_score = structure_score + 1
        print("Conclusion found")
    if 'references' in filtered_text:
        references_index = filtered_text.find('references')
        structure_score = structure_score + 1
        print("References found")

    if introduction_index != -1 and  (conclusion_index != -1 or references_index !=-1):
        if conclusion_index - introduction_index > 0 or references_index - introduction_index > 0:
            structure_score = structure_score +1
            print("Methods found")

    optional_structure_score = optional_structure(filtered_text)

    return structure_score


def optional_structure(page_text : str):
    if 'acknowledgments' in page_text or 'discussion':
        print("optional structure found")
        return 1
    return 0


def abstract_of_page(page_text : str):
    abstract = -1
    page_text = page_text.lower()
    '''
    used for structure analysis on first few pages
    :return:
    '''
    if 'abstract' in page_text:
        abstract = 1
        return abstract

