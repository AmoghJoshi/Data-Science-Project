import Tokenize as T
import os
import nltk

def has_numbers(value):
    for c in value:
        if c.isdigit():
            return 1
    return 0

def has_no_caps(value):
    if (not ' ' in value):
        if(len(value) == 0 or not value[0].isupper()):
            return 1
        else:
            return 0

    values = value.split(" ")
    for v in values:
        if (len(v) == 0 or not v[0].isupper()):
            return 1
    return 0

def is_token_negative(value, negative_words):
    if (not ' ' in value):
        if(value.lower() in negative_words):
            return 1
        else:
            for word in negative_words:
                if(word.lower().find(value.lower()) != -1):
                    return 1

        return 0

    values = value.split(" ")
    for v in values:
        if (v.lower() in negative_words):
            return 1;
    return 0;

def get_negative_words(READ_DIR):
    os.chdir(READ_DIR)
    negative_words = []
    for filename in os.listdir(os.getcwd()):
        file = open(filename, "r")
        content = file.readlines()
        content = [x.strip() for x in content]
        negative_words += content
    negative_words = [x.strip().lower() for x in negative_words]

    return negative_words

def remove_empty_tokens(n_gram):
    non_empty_tokens = []
    for token in n_gram:
        if (len(token.value) > 0):
            non_empty_tokens.append(token)
    return non_empty_tokens

def remove_numeric_tokens(n_gram):
    non_numeric = []
    for token in n_gram:
        if (not has_numbers(token.value)):
            non_numeric.append(token)
    return non_numeric

def remove_non_cap_tokens(n_gram):
    cap_tokens = []
    for token in n_gram:
        if (has_no_caps(token.value) == 0):
            cap_tokens.append(token)
    return cap_tokens

def remove_mixed_words(n_gram):
    non_mixed_tokens = []
    for token in n_gram:
        if((':' in token.value or ';' in token.value or ',' in token.value or '?' in token.value  or '!' in token.value)):
            continue
        non_mixed_tokens.append(token)
    n_gram = non_mixed_tokens
    return n_gram

def remove_negative_tokens(n_gram, negative_words):
    positive_tokens = []
    for token in n_gram:
        if (is_token_negative(token.value, negative_words) == 0):
            positive_tokens.append(token)
    return positive_tokens

def remove_non_noun(n_gram):
    noun_tags = ['nn', 'nnp', 'nns']
    valid_pos_tags=[]
    for token in n_gram:
        if (' ' in token.value):
            words = token.value.split(' ')
        else:
            words = [token.value]
        not_noun = 0
        for word in words:
            tag = nltk.pos_tag(word)

            if (not tag[0][1].lower() in noun_tags):
                not_noun = 1
                break
        if (not_noun == 0):
            valid_pos_tags.append(token)

    n_gram=valid_pos_tags
    return n_gram

def pre_process():
    f = open("mode", "r")
    mode = f.read()
    f.close()

    if (mode == '0'):
        READ_DIR = "clean_train_set"
    elif (mode == '1'):
        READ_DIR = "clean_test_set"


    one_gram = T.create_mono_gram(READ_DIR)
    two_gram = T.create_bi_gram(READ_DIR, one_gram)
    three_gram = T.create_tri_gram(READ_DIR, one_gram)
    n_gram_list1 = []
    READ_DIR = "Data"
    n_gram = one_gram + two_gram + three_gram
    negative_words = get_negative_words(READ_DIR)
    n_gram=remove_empty_tokens(n_gram)
    n_gram = remove_numeric_tokens(n_gram)
    n_gram=remove_non_cap_tokens(n_gram)
    n_gram=remove_negative_tokens(n_gram, negative_words)
    n_gram=remove_mixed_words(n_gram)
    os.chdir('..')
    return n_gram, one_gram