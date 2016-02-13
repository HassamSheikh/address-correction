import operator
import os
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
DATA_FILE_FOR_META_SEGMENTATION = 'word_segmentation_metaphone'
SEMI_STRUCTURED_ADDRESS_LIST    = 'semi_structured_address'

def extract_data_for_feeder(feeder_index, output_file):
  address_list = map(remove_digits_and_punctuations_from_string, DATA[DATA['50401'] == ALL_FEEDERS_LIST[feeder_index]][DATA.columns[9]].tolist())
  with open(output_file,'wb') as f:
    pickle.dump(address_list, f)

def remove_digits_and_punctuations_from_string(str):
  return str.translate(None, string.digits).translate(None, string.punctuation).lstrip()

def extract_semi_structured_addresses(address_file, segmentation_input_file, output_file):
  segment_data = segment.load_data_from_pickle_file(segmentation_input_file)
  segment.set_segmentation_data(segment_data, factor = 100)
  address_list = segment.read_pickle_for_segmentation_file(address_file)
  address_list = map(semi_structured_address, address_list)
  with open(output_file,'wb') as f:
    pickle.dump(address_list, f) 

def valid_word_based_on_metaphone_size(word):
  return word if len(doublemetaphone(word)[0]) > 1 else '' 

def semi_structured_address(address):
  return  re.sub(' +',' ', " ".join(map(valid_word_based_on_metaphone_size, segment.segment(re.sub(' +', '', address))))).lstrip()

def wordy(words):
 return [word for word in words if len(word) > 1]

def create_data_for_processing(feeder_number):
  extract_data_for_feeder(ALL_FEEDERS_LIST.index(feeder_number), ADDRESSES_FROM_SINGLE_FEEDER) if not os.path.isfile(ADDRESSES_FROM_SINGLE_FEEDER) else None
  addresses = segment.read_pickle_for_segmentation_file(ADDRESSES_FROM_SINGLE_FEEDER) 
  segment.extract_segmentation_file_from_text(addresses, DATA_FILE_FOR_WORD_SEGMENTATION, 1, 8) if not os.path.isfile(DATA_FILE_FOR_WORD_SEGMENTATION) else None
  segment.extract_segmentation_file_from_text(addresses, DATA_FILE_FOR_META_SEGMENTATION, 1, 8, metaphone = True) if not os.path.isfile(DATA_FILE_FOR_META_SEGMENTATION) else None
  extract_semi_structured_addresses(ADDRESSES_FROM_SINGLE_FEEDER, DATA_FILE_FOR_WORD_SEGMENTATION, SEMI_STRUCTURED_ADDRESS_LIST) if not os.path.isfile(SEMI_STRUCTURED_ADDRESS_LIST) else None

