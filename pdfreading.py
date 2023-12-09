from operator import itemgetter
import os

def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def fonts(doc, granularity=False):
    """Extracts fonts and their usage in PDF documents.
    :param doc: PDF document to iterate through
    :type doc: <class 'fitz.fitz.Document'>
    :param granularity: also use 'font', 'flags' and 'color' to discriminate text
    :type granularity: bool
    :rtype: [(font_size, count), (font_size, count}], dict
    :return: most used fonts sorted by count, font style information
    :example: font_counts, styles = fonts(doc, granularity=False)
[('9.5', 1079), ('10.0', 190), ('8.5', 28), ('10.5', 24), ...]
{'12.0': {'size': 12.0, 'font': 'ArialMT'}, '9.0': {'size': 9.0, 'font': 'XKZKVH+VAGRoundedStd-Light'}, ...}
    :explanation: he most used font-size is 9.5, with a count of 1079 text spans of this size.
    It is very likely that this font-size represents the paragraphs in our document.
    """
    styles = {}
    font_counts = {}

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if granularity:
                            identifier = "{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                            styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                                  'color': s['color']}
                        else:
                            identifier = "{0}".format(s['size'])
                            styles[identifier] = {'size': s['size'], 'font': s['font']}

                        font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage
            else:
                pass

    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles

def font_tags(font_counts, styles):
    """Returns dictionary with font sizes as keys and tags as value.
    This will allow us to discriminate headers, paragraphs and subscriptors through fontsize
    :param font_counts: (font_size, count) for all fonts occuring in document
    :type font_counts: list
    :param styles: all styles found in the document
    :type styles: dict
    :rtype: dict
    :return: all element tags based on font-sizes
    :example:{60.0: '<h1>', 59.69924545288086: '<h2>', 36.0: '<h3>', 30.0: '<h4>', 24.0: '<h5>', 20.0: '<h6>', 16.0: '<h7>', 14.0: '<h8>', 13.0: '<h9>', 10.5: '<h10>', 10.0: '<h11>', 9.5: '<p>', 9.452380180358887: '<s1>', 9.404520988464355: '<s2>', 8.5: '<s3>', 8.0: '<s4>', 7.5: '<s5>', 7.0: '<s6>'}
    """
    p_style = styles[font_counts[0][0]]  # get style for most used font by count (paragraph)
    p_size = p_style['size']  # get the paragraph's size

    # sorting the font sizes high to low, so that we can append the right integer to each tag
    font_sizes = []
    for (font_size, count) in font_counts:
        font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)

    # aggregating the tags for each font size
    idx = 0
    size_tag = {}
    for size in font_sizes:
        idx += 1
        if size == p_size:
            idx = 0
            size_tag[size] = '<p>'
        if size > p_size:
            size_tag[size] = '<h{0}>'.format(idx)
        elif size < p_size:
            size_tag[size] = '<s{0}>'.format(idx)

    return size_tag

def headers_para(doc, tag):
    """Scrapes headers & paragraphs from PDF and return texts with element tags.
    :param doc: PDF document to iterate through
    :type doc: <class 'fitz.fitz.Document'>
    :param size_tag: textual element tags for each size
    :type size_tag: dict
    :rtype: list
    :return: texts with pre-prended element tags
    """
    header_para = []  # list with headers and paragraphs
    first = True  # boolean operator for first header
    previous_s = {}  # previous span

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # this block contains text

                # REMEMBER: multiple fonts and sizes are possible IN one block

                block_string = ""  # text found in block
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if tag[s['size']] == '<h{0}>' or tag[s['size']] == '<p>':
                            if s['text'].strip():  # removing whitespaces:
                                if first:
                                    previous_s = s
                                    first = False
                                    block_string = s['text']
                                else:
                                    if s['size'] == previous_s['size']:

                                        if block_string and all((c == "|") for c in block_string):
                                            # block_string only contains pipes
                                            block_string = s['text']
                                        if block_string == "":
                                            # new block has started, so append size tag
                                            block_string = s['text']
                                        else:  # in the same block, so concatenate strings
                                            block_string += " " + s['text']

                                    else:
                                        header_para.append(block_string)
                                        block_string = s['text']

                                    previous_s = s

                        # new block started, indicating with a pipe
                        #block_string += "|"

                header_para.append(block_string)

    return header_para
