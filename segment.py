"""
English Word Segmentation in Python

Word segmentation is the process of dividing a phrase without spaces back
into its constituent parts. For example, consider a phrase like "thisisatest".
For humans, it's relatively easy to parse. This module makes it easy for
machines too. Use `segment` to parse a phrase into its parts:

>>> from wordsegment import segment
>>> segment('thisisatest')
['this', 'is', 'a', 'test']
"""
import sys
from math import log10
from functools import wraps
import re
from collections import Counter
import operator
import codecs
import pickle
from metaphone import doublemetaphone

if sys.hexversion < 0x03000000:
    range = xrange

unigram_counts,bigram_counts, total_count = ("",) * 3

def read_text_for_segmentation_file(input_file):
    return codecs.open(input_file, 'r').read().lower()

def read_pickle_for_segmentation_file(filename):
    with open(filename, 'rb') as handle:
        words = pickle.load(handle)
    return map(str.lower, words)
  
def dump_into_pickle_file(output_file, word_counts):
    with open(output_file, 'wb') as handle:
        pickle.dump(dict(word_counts), handle)

def word_count(text, min_size, max_size, flag):
    if isinstance(text, list):
        text = ''.join(text)
    return Counter([word_or_metaphone(word, flag) for word in re.findall(r'\w+', text) if (len(word) < (abs(max_size) + 1) and len(word) > (abs(min_size) - 1) and not unicode(word, 'utf-8').isnumeric())])

def extract_segmentation_file_from_text(text, output_file, min_size, max_size, **kwargs):
    word_counts   = word_count(text, min_size, max_size, True) if kwargs.get('metaphone') else word_count(text, min_size, max_size, False) 
    dump_into_pickle_file(output_file, word_counts)

def word_or_metaphone(word, flag):
    return get_metaphone_from_word(word) if flag else word
  
def load_data_from_pickle_file(filename):
    with open(filename, 'rb') as handle:
        words = pickle.load(handle)
    return words

def get_metaphone_from_word(word):
  return doublemetaphone(word)[0] if len(doublemetaphone(word)[0]) > 1 else doublemetaphone(word)[1]

def load_data_from_text_file(filename):
    """Read `filename` and parse tab-separated file of (word, count) pairs."""
    with open(filename) as fptr:
        lines = (line.split('\t') for line in fptr)
        return dict((word, number) for word, number in lines)

def change_data_values_to_float(data, factor):
    return {key: float(value * factor) for key, value in data.items()}

def memoize(func):
    """Memoize arguments to function `func`."""
    cache = dict()
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def divide(text, limit=50):
    for pos in range(1, min(len(text), limit) + 1):
        yield (text[:pos], text[pos:])

def score(word, prev=None):
    if prev is None:
        if word in unigram_counts:
            return unigram_counts[word] / total_count
        else:
            return 10.0 / (total_count * 10 ** len(word))
    else:
        bigram = '{0} {1}'.format(prev, word)
        if bigram in bigram_counts and prev in unigram_counts:
            return bigram_counts[bigram] / total_count / score(prev)
        else:
            return score(word)

def set_segmentation_data(segment_data, **kwargs):
    global unigram_counts, total_count, bigram_counts
    factor                        = kwargs.get('factor') if kwargs.get('factor') > 1 else 1
    unigram_counts, bigram_counts = (change_data_values_to_float(segment_data, factor),) * 2
    total_count                   = sum(unigram_counts.values())

def segment(text, **kwargs):
    factor                        = kwargs.get('factor') if kwargs.get('factor') > 1 else 1
    if bool(unigram_counts) is False or 'segment_data' in kwargs:
        set_segmentation_data(kwargs.get('segment_data'), factor = factor)
    
    @memoize
    def search(text, prev='<S>'):
        if text == '':
            return 0.0, []

        def candidates():
            for prefix, suffix in divide(text):
                prefix_score = log10(score(prefix, prev))
                suffix_score, suffix_words = search(suffix, prefix)
                yield (prefix_score + suffix_score, [prefix] + suffix_words)

        return max(candidates())

    result_score, result_words = search(text)

    return result_words