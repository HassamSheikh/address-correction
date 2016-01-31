import re
from collections import Counter
import operator
import codecs
import pickle
from metaphone import doublemetaphone

ADDRESSES_FROM_SINGLE_FEEDER ='feeder'
DATA_FILE_FOR_WORD_SEGMENTATION = 'word_segmentation'

text        = codecs.open('feeder', 'r').read()

def get_metaphone_from_word(word):
  return doublemetaphone(word)[0] if len(doublemetaphone(word)[0]) > 1 else doublemetaphone(word)[1]

def word_count(text, min_size, max_size):
    return Counter([get_metaphone_from_word(word.lower()) for word in re.findall(r'\w+', text) if (len(word) < (abs(max_size) + 1) and len(word) > (abs(min_size) - 1) and not unicode(word, 'utf-8').isnumeric())])