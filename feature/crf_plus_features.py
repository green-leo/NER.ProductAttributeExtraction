# ----------------------------------------------------------------------------------------------------------------------- #
# define keywords based on datat review 
# ----------------------------------------------------------------------------------------------------------------------- #

lst_linkword = ['và', 'với', 'and']

lst_type = {1: ['combo', 'set', 'bộ', 'đồ', 'hũ', 'hộp', 'chai', 'máy', 'vỉ'],
            2: ['dụng cụ', 'phụ kiện', 'thiết bị']}

lst_brand = {'1_prefix': ['hiệu', 'hãng'],
             2: ['việt nhật'],
             '2_prefix': ['thương hiệu']}

lst_origin = {1: ['xuất', 'nhập', 'qc', 'tq', 'hàn', 'vnxk'],
              2: ['nội địa', 'hàng nhập', 'hàng xuất', 'nhập khẩu', 'xuất khẩu', 'tiêu chuẩn', 'chính hãng'],
              3: ['hàng xuất khẩu', 'hàng nhập khẩu']}

lst_form = {'1_prefix': ['form', 'mẫu', 'dáng', 'style', 'phom'],
            '1_suffix': ['design', 'style'],
            2: ['phong cách', 'thiết kế', 'kiểu dáng', 'design by', 'designed by']}

lst_color = {1: ['màu'],
             2: ['nhiều màu', 'chọn màu', 'màu sắc']}





# ----------------------------------------------------------------------------------------------------------------------- #
# isFeature function
# ----------------------------------------------------------------------------------------------------------------------- #

# is in a list of keyword
def is_keyword(lst_words, lst_keywords):
    if ' '.join(lst_words) in lst_keywords:
        return True
    return False

# is a number (float + integer)
def isDigit(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# a combine of digits and letters
def isCode(word):
    if any([c.isdigit() for c in word]) and any([c.isalpha() for c in word]):
        return True
    return False

# name
def is_name_code(word):
    if isCode(word)\
        or (word in ['ms', 'mã', 'bản'])\
        or (word.isdigit() and len(word)>=4):
            return True
    return False

def is_name_2w(word1, word2):
    if ' '.join([word1, word2]) in ["mã số", "phiên bản"]:
        return True
    elif word1 in ['ms', 'mã', 'bản'] and isCode(word2):
        return True
    return False

# color
def is_color_2w(word1,word2):
    if word1.isdigit() and word2 == 'màu':
        return True
    elif word1 == 'màu' and (word2.isdigit() or isCode(word2)):
        return True
    return False




# ----------------------------------------------------------------------------------------------------------------------- #
# Word to Features
# ----------------------------------------------------------------------------------------------------------------------- #

def word2features(sent, i):
    # sent : (word, postag, label)
    word = sent[i][0]
    postag = sent[i][1]

    # current word : position 0
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'is_type_prefix_1w' : is_keyword([word], lst_type[1]),
        'is_brand_prefix_1w' : is_keyword([word], lst_brand['1_prefix']),
        'is_name_code' : is_name_code(word),
        'is_origin_1w' : is_keyword([word], lst_origin[1]),
        'is_form_prefix_1w' : is_keyword([word], lst_form['1_prefix']),
        'is_form_suffix_1w' : is_keyword([word], lst_form['1_suffix']),
        'is_color_1w' : is_keyword([word], lst_color[1]),
    }


    # word - 1 : position - 1
    # or BOS : begining of sentences
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:is_and_word' : is_keyword([word1], lst_linkword),
            '-1:is_type_prefix_1w' : is_keyword([word1], lst_type[1]),
            '-1:is_brand_prefix_1w' : is_keyword([word1], lst_brand['1_prefix']),
            '-1:is_brand_2w' : is_keyword([word1,word], lst_brand[2]),
            '-1:is_origin_1w' : is_keyword([word1], lst_origin[1]),
            '-1:is_origin_2w' : is_keyword([word1,word], lst_origin[2]),
            '-1:is_form_prefix_1w' : is_keyword([word1], lst_form['1_prefix']),
            '-1:is_form_2w' : is_keyword([word1,word], lst_form[2]),
            '-1:is_color_1w' : is_keyword([word1], lst_color[1]),
            '-1:is_color_2w' : is_color_2w(word1,word),

        })
    else:
        features['BOS'] = True


    # word + 1 : position + 1
    # or EOS : ending of sentences
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:is_brand_2w' : is_keyword([word,word1], lst_brand[2]),
            '+1:is_origin_1w' : is_keyword([word1], lst_origin[1]),
            '+1:is_origin_2w' : is_keyword([word,word1], lst_origin[2]),
            '+1:is_form_suffix_1w' : is_keyword([word1], lst_form['1_suffix']),
            '+1:is_color_2w' : is_color_2w(word,word1),
        })
    else:
        features['EOS'] = True


    # word - 2 : position - 2
    if i > 1:
        word1 = sent[i-1][0]
        word2 = sent[i-2][0]
        postag2 = sent[i-2][1]
        features.update({
            '-2:word.lower()': word2.lower(),
            '-2:word.istitle()': word2.istitle(),
            '-2:word.isupper()': word2.isupper(),
            '-2:postag': postag2,
            '-2:is_type_prefix_1w' : is_keyword([word2], lst_type[1]),
            '-2:is_type_prefix_2w' : is_keyword([word2,word1], lst_type[2]),
            '-2:is_brand_prefix_1w' : is_keyword([word2], lst_brand['1_prefix']),
            '-2:is_brand_prefix_2w' : is_keyword([word2,word1], lst_brand['2_prefix']),
            '-2:is_name_2w' : is_name_2w(word2,word1),
            '-2:is_origin_1w' : is_keyword([word2], lst_origin[1]),
            '-2:is_origin_2w' : is_keyword([word2,word1], lst_origin[2]),
            '-2:is_origin_3w' : is_keyword([word2,word1,word], lst_origin[3]),
            '-2:is_form_prefix_1w' : is_keyword([word2], lst_form['1_prefix']),
            '-2:is_form_2w' : is_keyword([word2,word1], lst_form[2]),
            '-2:is_color_1w' : is_keyword([word2], lst_color[1]),
            '-2:is_color_2w' : is_color_2w(word2,word1),

        })


    # word + 2 : postion + 2
    if i < len(sent)-2:
        word1 = sent[i+1][0]
        word2 = sent[i+2][0]
        postag2 = sent[i+2][1]
        features.update({
            '+2:word.lower()': word2.lower(),
            '+2:word.istitle()': word2.istitle(),
            '+2:word.isupper()': word2.isupper(),
            '+2:postag': postag2,
            '+2:is_origin_1w' : is_keyword([word2], lst_origin[1]),
            '+2:is_origin_2w' : is_keyword([word1,word2], lst_origin[2]),
            '+2:is_origin_3w' : is_keyword([word,word1,word2], lst_origin[3]),
            '+2:is_form_suffix_1w' : is_keyword([word2], lst_form['1_suffix']),
            '+2:is_color_2w' : is_color_2w(word1,word2),
        })


    # middle word : position (-1, 0, +1)
    # sequence freature
    if i > 0 and i < len(sent)-1:
        word1 = sent[i-1][0]
        word2 = sent[i+1][0]
        features.update({
            '-3:is_origin_3w' : is_keyword([word1,word,word2], lst_origin[3]),
        })



    return features