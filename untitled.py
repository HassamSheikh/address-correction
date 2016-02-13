import codecs
import operator
import pandas
import pickle
import re
import segment
import string
import time
from metaphone import doublemetaphone
from collections import Counter

DATA                            = pandas.read_csv("lahore.csv")
ALL_FEEDERS_LIST                = sorted(DATA['50401'].unique())
ADDRESSES_FROM_SINGLE_FEEDER    = 'feeder'
DATA_FILE_FOR_WORD_SEGMENTATION = 'word_segmentation'

def extract_data_for_feeder(feeder_index):
  address_list = map(remove_digits_and_punctuations_from_string, DATA[DATA['50401'] == ALL_FEEDERS_LIST[feeder_index]][DATA.columns[9]].tolist())
  with open(ADDRESSES_FROM_SINGLE_FEEDER,'wb') as f:
    pickle.dump(address_list, f)

def remove_digits_and_punctuations_from_string(str):
  return str.translate(None, string.digits).translate(None, string.punctuation).lstrip()


def create_data_for_processing(feeder_number):
  extract_data_for_feeder(ALL_FEEDERS_LIST.index(feeder_number))
  addresses = segment.read_pickle_for_segmentation_file(ADDRESSES_FROM_SINGLE_FEEDER)
  segment.extract_segmentation_file_from_text(addresses, DATA_FILE_FOR_WORD_SEGMENTATION, 2, 8)

