#!/usr/bin/env python
# coding: utf-8


import re, unicodedata


def labels_sort_func(label):
    return label[0]



def remove_index_cate(text):
    sIndex = text.find('[')
    eIndex = text.find(']', sIndex)
    if sIndex == 0 and eIndex != -1 and text[sIndex+1:eIndex].isnumeric():
        text = text[eIndex+1:].strip()
    else:
        return text
    
    sCate = text.find('[')
    eCate = text.find(']', sCate)
    if sCate == 0 and eCate != -1 and text[sCate+1:eCate].isnumeric():
        text = text[eCate+1:].strip()
    else:
        return text
    
    return text



from viet_text_tools import normalize_diacritics

def remove_urls(text):
    URL_RE = re.compile(r'(http[s]?://|www.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return URL_RE.sub('', text)

def remove_text_tags(text):
    # TEXT_TAG_RE = re.compile(r'#[a-zA-Z0-9-_àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]+')
    # return TEXT_TAG_RE.sub('', text)
    text = text.replace('#', '')
    return text

def clean_special_chars(text):
    text = text.replace('&nbsp', ' ').replace('& nbsp', ' ').replace('xa0', ' ').replace('&gt',' ').replace('&lt',' ')
    text = re.sub('[^a-zA-Z0-9.àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ \+\-\%\,\<\/\>]+', ' ', text)
    text = ' '.join(text.split())
    return text

# Normalize text with 'NFKC'
def normalize_text(text):
    return unicodedata.normalize('NFKC', text)

#lst_skip = ['nam', 'nữ', 'combo', 'những', 'hoặc']

def title_unify(prod):
    title = remove_text_tags(remove_urls(normalize_diacritics(normalize_text(prod.strip()))))
    title = clean_special_chars(title)
    title = ' '.join(title.split())
    return title


