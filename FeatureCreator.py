import PreProcessor as pp
from PreProcessor import has_no_caps
import nltk
import numpy as np

def hasNumbers(ngrams):
    for c in ngrams:
        if c.isdigit():
            return 1
    return 0


def get_actual_labels(n_gram_list):
    actual_labels = []
    for tok in n_gram_list:
        if (tok.is_name == 0):
            actual_labels.append(0)
        else:
            actual_labels.append(1)
    return actual_labels


def make_features():
    feature_caps = []
    feature_all_caps = []
    feature_has_numbers = []
    feature_middle_singlecap = []
    feature_prefix_article = []
    feature_suffix_caps = []
    feature_biprefix_caps = []
    feature_bisuffix_caps = []
    feature_prefix_caps = []
    feature_prefix_email = []
    feature_prefix_greeting = []
    feature_suffix_write = []
    feature_comma = []
    feature_full_stop = []
    feature_s = []
    feature_wordlength = []
    feature_period = []


    write_list = ['writes', 'wrote']
    greetings = ['regards', 'thanks', 'cheers', 'greetings', 'beastmaster']
    email_ids = ['edu', 'com', 'net', 'ca']

    n_gram_list, mono_gram  = pp.pre_process()

    for n_gram in n_gram_list:
        if (n_gram.value.isupper()):
            feature_all_caps.append(1)
        else:

            feature_all_caps.append(0)

        if (' ' in n_gram.value):
            words = n_gram.value.split(' ')
            if (len(words) == 3 and len(words[1]) == 1 and words[1].isupper()):
                feature_middle_singlecap.append(1)
            else:
                feature_middle_singlecap.append(0)
        else:
            feature_middle_singlecap.append(0)

        if (hasNumbers(n_gram.value) == 1):
            feature_has_numbers.append(0)
        else:
            feature_has_numbers.append(1)

        index = n_gram.index
        if (index >= 1):
            prefix1 = mono_gram[index - 1]
            if (prefix1.value.lower() == 'a' or prefix1.value.lower() == 'an' or prefix1.value.lower() == 'the'):
                feature_prefix_article.append(0)
            else:
                feature_prefix_article.append(1)
        else:
            feature_prefix_article.append(1)

        index = n_gram.index
        if (index >= 1):
            prefix1 = mono_gram[index - 1]
            if (len(prefix1.value) > 0  and prefix1.value[0].isupper()):
                feature_prefix_caps.append(0)
            else:
                feature_prefix_caps.append(1)
        else:
            feature_prefix_caps.append(1)

        index = n_gram.index
        if (index >= 1):
            prefix1 = mono_gram[index - 1]
            if (prefix1.value.lower() in email_ids):
                feature_prefix_email.append(1)
            else:
                feature_prefix_email.append(0)
        else:
            feature_prefix_email.append(0)

        index = n_gram.index
        if (index >= 1):
            prefix1 = mono_gram[index - 1]
            if (prefix1.value.lower() in greetings):
                feature_prefix_greeting.append(1)
            else:
                feature_prefix_greeting.append(0)
        else:
            feature_prefix_greeting.append(0)

        index = n_gram.index
        length = 1
        if (' ' in n_gram.value):
            length = len(n_gram.value.split(" "))
        if (index < len(mono_gram) - length):
            suffix1 = mono_gram[index + length]
            if (suffix1.value.lower() in write_list):
                feature_suffix_write.append(1)
            else:
                feature_suffix_write.append(0)
        else:
            feature_suffix_write.append(0)

        index = n_gram.index
        length = 1
        if (' ' in n_gram.value):
            length = len(n_gram.value.split(" "))
        if (index < len(mono_gram) - length):
            suffix1 = mono_gram[index + length]
            if (len(suffix1.value)  and suffix1.value[0].isupper()):
                feature_suffix_caps.append(0)
            else:
                feature_suffix_caps.append(1)
        else:
            feature_suffix_caps.append(1)

        index = n_gram.index
        length = 1
        if (' ' in n_gram.value):
            length = len(n_gram.value.split(" "))
        if (index < len(mono_gram) - length):
            suffix1 = mono_gram[index + length]
            if (suffix1.value.lower() == 's'):
                feature_s.append(1)
            else:
                feature_s.append(0)
        else:
            feature_s.append(0)

        index = n_gram.index
        length = 1
        if (' ' in n_gram.value):
            length = len(n_gram.value.split(" "))
        if (index < len(mono_gram) - length):
            suffix1 = mono_gram[index + length].value
            if ('?' in suffix1 or ':' in suffix1 or '!' in suffix1 or ';' in suffix1):
                feature_full_stop.append(1)
            else:
                feature_full_stop.append(0)
        else:
            feature_full_stop.append(0)

        index = n_gram.index
        if (index > 1):
            if (',' in mono_gram[index - 1].value or ';' in mono_gram[index-1].value or ':' in mono_gram[index-1].value):
                feature_comma.append(1)
            else:
                feature_comma.append(0)
        else:
            feature_comma.append(0)

        feature_caps.append(has_no_caps(n_gram.value))
        length = len(n_gram.value.split(" "))
        if (not '' in n_gram.value):
            feature_wordlength.append(1)
        elif length > 2:
            feature_wordlength.append(0)
        else:
            feature_wordlength.append(1)

        if ('.' in n_gram.value):
            feature_period.append(0)
        else:
            feature_period.append(1)

    return [feature_period, feature_full_stop, feature_comma, feature_prefix_caps, feature_suffix_caps, feature_all_caps, feature_has_numbers,
            feature_middle_singlecap, feature_prefix_article, feature_prefix_email, feature_prefix_greeting,
            feature_suffix_write, feature_s], n_gram_list
