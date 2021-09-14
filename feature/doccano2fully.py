#!/usr/bin/env python
# coding: utf-8

import os
import json
from bs4 import BeautifulSoup
from bs4.element import Tag
from feature.clean_text import *
#from clean_text import *


# ### Convert doccano annotation format to fully annotation slices format
# #### doccano format: 
# ##### {"text": text_string, "labels": [[strat_offset, end_offset, label], ...]}
# - eg: {"text": "[9] hàng nhập áo sơ mi  nữ cao cấp kiểu dáng sang chảnh", "labels": [[14, 22, "type"], [23, 25, "gender"]]}
# - start_offset: index of the first letter of the entry token
# - end_offset: index of the letter after the entry token (index of the last letter + 1)
# - the entry token = text_string[start_offset:end_offset]
# 
# #### fully slices format: 
# ##### {"content": text_string, "annotation": [{"label":[label], "points": [{"start":start_index,"end":end_index,"text":token}]}, ...]}
# - eg: {"content":"[9] hàng nhập áo sơ mi  nữ cao cấp kiểu dáng sang chảnh", 
#         "annotation":[
#         ...,
#         {"label":["type"],"points":[{"start":14,"end":15,"text":"áo"}]},
#         {"label":["type"],"points":[{"start":17,"end":18,"text":"sơ"}]},
#         {"label":["type"],"points":[{"start":20,"end":21,"text":"mi"}]},
#         ...,
#         {"label":["gender"],"points":[{"start":23,"end":25,"text":"nữ"}]},
#         ...'
#         {"label":["None"],"points":[{"start":50,"end":55,"text":"chảnh"}]}]
#        }
# - start_index = start_offset
# - end_index = end_offset - 1
# - token = text_string[start_index:end_index+1]
# 
# #### The base differents: 
# ##### the fully format is about slicing evey token to very each words
# ##### and annotating none labeld word
# - eg: [áo sơ mi, type] -> [[áo - type], [sơ - type], [mi - type]]
# - eg: none labeled token "chảnh" in doccano format is annotated in fully format
# 
# #### Steps by Steps
# - Convert doccano to html for easyly extracting by BeautifulSoup
# - Convert html to fully by reading each tokens, words
# 
# ***

# #### Doccano To Html


def doccano2html(doccano_annot_str):
    doccano_annot = json.loads(doccano_annot_str)
    text_label = ''
    text = doccano_annot['text']
    labels = doccano_annot['labels']
    labels.sort(reverse = True, key = labels_sort_func)
    
    #have been not annotated yet
    if len(labels) == 0:
        return text_label
    
    #convertation
    text_label = text
    for label_elem in labels:
        sIndex, eIndex, label = label_elem
        text_prefix = text_label[:sIndex]
        text_label = text_prefix + ' <' + label + '>' + text_label[sIndex:eIndex].strip() + '</'+ label + '> ' + text_label[eIndex:].strip()
    
    text_label = (' '.join(text_label.split()))
    return text_label


# #### Html to Fully

#convert html to fully
#{"content": text_string, "annotation": [{"label":[label], "points": [{"start":start_index,"end":end_index,"text":token}]}, ...]}

def html2fully(html_annot):
    soup = BeautifulSoup(html_annot,  "html.parser")
    title_text = soup.text

    annotation = []
    pre_index = 0

    for c in soup:
        #there is space -> skip
        token = c.string.strip()
        if isinstance(token, str) == False or token == None or token == '':
            continue
        if (type(c) == Tag):
            label = c.name.lower()
        else:
            label = 'None'
            
        for word in token.split():
            start_index = title_text.find(word, pre_index)
            if (start_index == -1):
                print("#there's something wrong: " + word)
                print("#title: " + title_text)
                continue

            end_index = start_index + len(word) - 1
            annotation.append({"label":[label], "points": [{"start":start_index,"end":end_index,"text":word}]})
            pre_index = end_index

    fully_format = {"content": title_text, "annotation":annotation}
    return json.dumps(fully_format, ensure_ascii=False) + '\n'


# #### Doccano to Fully

def doccano2fully(doccano_annot):
    html_annot = doccano2html(doccano_annot)
    html_annot = remove_index_cate(html_annot)
    html_annot = title_unify(html_annot)
    fully_annot = html2fully(html_annot)
    return fully_annot



# #### Extract fully annotations
# ##### return:
# - text: the string input
# - labels: the array of all labels in the annotation
# - annots: thay array of all pairs (word, label) in the annotation

def extract_fully_data(fully_annot_str):
    fully_annot_json = json.loads(fully_annot_str)
    text = fully_annot_json['content']
    annotations = fully_annot_json['annotation']
    tagged = False
    labels = []
    words = []
    if (annotations is not None) and (len(annotations) != 0):
        tagged = True
        for annotation in annotations:
            label = annotation['label'][0]
            word = annotation['points'][0]['text']
            labels.append(label)
            words.append(word)
            
    return text, labels, words, tagged




# ***
# #### Testing

# doccano_annot = '{"text": "[9] hàng nhập áo sơ mi nữ cao cấp kiểu dáng sang chảnh", "labels": [[14, 22, "type"], [23, 25, "gender"]]}'
# print(doccano2fully(doccano_annot))

