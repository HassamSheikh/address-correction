import pandas
import re
import os
import errno
from string import *
from collections import Counter
import operator
import functools, math
import sys
import py_compile
import shutil
import nltk
from metaphone import *
from jellyfish import jaro_distance
from jellyfish import levenshtein_distance
import jellyfish
import numpy
import csv
import pickle
import time
try : 
	os.remove('segment.pyc')
except:
	print ' not found'

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



def word_cluster(text1):
	vocab_dict = dict()
		
	if os.path.isfile('MetaphoneCluster.txt'):
		output = open('MetaphoneCluster.txt', 'rb')
		vocab_dict = pickle.load(output) 
	else:
		Fdist= nltk.FreqDist(final_word(text1)) 
		sorted_x = Fdist.items()
		#sorted_x = sorted(listkeys, key=operator.itemgetter(0))
		metaph_list=[]
		for x in xrange (len(sorted_x)):
			answer = doublemetaphone(sorted_x[x][0])
			if (len(answer[0])>1):
				metaph=answer[0]
			else:
				metaph=answer[1]
			if(vocab_dict.has_key(metaph)):
				4+4
			else:
				vocab_dict[metaph]=dict() 
			for y in xrange(x, len(sorted_x)):
				answer_temp = doublemetaphone(sorted_x[y][0])
				if (len(answer_temp[0])>1):
					metaph_temp=answer_temp[0]
				else:
					metaph_temp=answer_temp[1]
				if(metaph==metaph_temp):
					temp_dict=dict()
					temp_dict = vocab_dict[metaph]
					temp_dict[sorted_x[y][0]]=sorted_x[y][1]
					vocab_dict[metaph]=temp_dict
		output = open('MetaphoneCluster.txt', 'ab+')
		pickle.dump(vocab_dict, output)
		output.close()

	return vocab_dict
def final_word(text1):
	final1 =" ".join(text1)
	final=final1.split(' ')
	return final

def MaxiMumInVocab(dictionary,meta): 
	new_temp_list=[]
	if(dictionary.has_key(meta)):
		new_temp_dict=dictionary[meta]
		new_temp_list = new_temp_dict.items()
		new_temp_list = sorted(new_temp_list, key=operator.itemgetter(1),reverse=True)
	else:
		new_temp_list=['nothing','0']
	return new_temp_list[0]
def DictionaryCreation(vocab_dict):
	py_compile.compile('segmentmeta.py')
	from segmentmeta import segmentamt
	new_temp=[] 
  	seg_list=[]
  	file =open(vocab_dict_file,'w')
  	for key in vocab_dict:
  		new_temp.append(key)
  	new_temp=sorted(new_temp)# sorted keys of the clustered word dictionary
  	final_dict = dict()
  	for x in xrange (1, len(new_temp)):
  		seg = (segmentamt(new_temp[x]))
  		seg_list.append(seg)
  		for y in xrange(len(seg)):
  			final_vo=[]
  			final_vo = MaxiMumInVocab(vocab_dict,seg[y].upper()) 
    		if(final_dict.has_key(final_vo[0])==False):
    			final_dict[final_vo[0]]=final_vo[1]
    			file.write(str(final_vo[0])+'\n')
	file.close()
def AddressCheck(HamazaQuery,DictionaryFile):
	file = open(vocab_dict_file,'r')
	wordlist = file.readlines()
	file.close()
	final_sentence=HamazaQuery
	#text = ReturnLongAddressString(sentence)	
	clustered_words = DictionaryFile
	try:
		del clustered_words['']
	except:
		2+2
	if os.path.isfile(abb_list_file):
		with open(abb_list_file) as ab:
			abbrivate=ab.readlines()
	else:
		shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/'+abb_list_file,os.getcwd())
		with open(abb_list_file) as ab:
			abbrivate=ab.readlines()
	abb_list = CreateAbbList(abbrivate)
	correc_answer = []
	try:
		Query = PrepareFinalString(final_sentence,clustered_words,wordlist,abb_list,DictionaryFile)
		Query=Query.translate(None,punctuation)
		Query_split =Query.split(' ')
		for y in xrange(len(Query_split)):
			try:
				correc_answer.append ((SpellCheck(Query_split[y],wordlist)[0][0]))
			except:
				2+2	 
	except:
			2+2
	return(" ".join(correc_answer))

def PrepareFinalString(Address,cluster,wordlist,abb_list,vocab_dict):
	from segmentmeta import segmentamt
	from segment import segment
	xyz_score=45
	print(Address)
	Address =Address.lower()
	Address = (''.join( abb_list.get( word, word ) for word in re.split( '(\W+)', Address )) )
	Address = re.sub('[^A-Za-z]+',' ', Address) #extracting on alphabets
	Address= Address.split(' ') #removing all white spaces to make a single long query for segmentation i.e ahmedblockgardentown 
	I_do_not_have_anymore_names=[]	
	for k in xrange(len(Address)):
		temp_segment = segment(Address[k])
		print temp
		if(len(temp_segment)>1):
			for x in xrange(len(temp_segment)):
				answer = doublemetaphone(temp_segment[x])
				if (len(answer[0])>1):
					metaph=answer[0]
					if(cluster.has_key(metaph.upper())):
						I_do_not_have_anymore_names.append(str(MaxiMumInVocab(cluster,metaph.upper())[0]))
					else:
						I_do_not_have_anymore_names.append(str(temp_segment[x]))
				else:
					metaph=answer[1]
					if(cluster.has_key(metaph.upper())):
						I_do_not_have_anymore_names.append(str(MaxiMumInVocab(cluster,metaph.upper())[0]))
					else:
						I_do_not_have_anymore_names.append(str(temp_segment[x]))
				#if not metaph:
					#I_do_not_have_anymore_names.append(temp_segment[x])
		elif (len(temp_segment)==1):
			if(len(temp_segment[0])==1):
				I_do_not_have_anymore_names.append(temp_segment[0])
			else:
				Match_score = SpellCheck(temp_segment[0],wordlist)
				xyz_score = (float(Match_score[0][1])*100)
				if(xyz_score<85):
					answer = doublemetaphone(temp_segment[0])
					if (len(answer[0])>1):
						metaph=answer[0]
					else:
						metaph=answer[1]
					if not metaph:
						I_do_not_have_anymore_names.append(str(temp_segment[0]))
					segmented_meta=(segmentamt(metaph))
				#print (segmented_meta)
					for y in xrange(len(segmented_meta)):
						if(cluster.has_key(segmented_meta[y].upper())):
							I_do_not_have_anymore_names.append(str(MaxiMumInVocab(cluster,segmented_meta[y].upper())[0]))
						else:
							I_do_not_have_anymore_names.append(str(temp_segment))
				else:
					I_do_not_have_anymore_names.append(str(Match_score[0][0]))
		#print(I_do_not_have_anymore_names)
	Address =" ".join(I_do_not_have_anymore_names)
	Address = (''.join( abb_list.get( word, word ) for word in re.split( '(\W+)', Address )) )
	try:
		remove_list = RemoveList(vocab_dict)
		Address = (''.join( remove_list.get( word, word ) for word in re.split( '(\W+)', Address)))
	except:
		Address= re.sub(' +',' ',Address)
	return Address.strip()
def CreateAbbList(list_abb):
	abb_list= dict()
	for x in xrange(len(list_abb)):
	#	print (list_abb[x])
		abb_list[list_abb[x].rstrip().split('\t')[0]]=list_abb[x].rstrip().split('\t')[1]
	return abb_list	

def RemoveList(list_vocab_dic):
	new_temp=dict()
	remove_list= list_vocab_dic['']
	for key in remove_list:
		new_temp[key]=''
	return new_temp	
