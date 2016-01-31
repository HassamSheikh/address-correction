import re
from collections import Counter
import operator
import codecs
import pickle
from metaphone import doublemetaphone
import time
from segment import segment

ADDRESSES_FROM_SINGLE_FEEDER ='feeder'
DATA_FILE_FOR_WORD_SEGMENTATION = 'word_segmentation'

text = open('feeder','r').read().lower().splitlines()

def ReturnLongAddressString(sentence):
  text1=[]
  for x in xrange(len(sentence)):
    temp_segment = segment(sentence[x])# segmented words using Naive Bayes 
    sentence[x]= re.sub(' +',' '," ".join(wordy(temp_segment))).strip()
    text1.append(sentence[x]) #creating final address strin
  return text1

def semi_structured_address(address):
  return " ".join(wordy(re.sub(' +',' '," ".join(wordy(segment(re.sub('[^A-Za-z]+',' ', sentence))))).split(' ')))

def wordy(words):
 return [word for word in words if len(word) > 1]


time0 = time.time()
k = map(do_shit, text)
#k = ReturnLongAddressString(text)
time1= time.time()
print ('Time Taken to run this code is '+ str(time1-time0))
