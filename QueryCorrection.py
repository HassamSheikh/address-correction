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
data = pandas.read_csv("lahore.csv")	
all_feeders = sorted(data['50401'].unique())
SingleFeederAddresses='SingleFeederAddresses'
SegmentFile= 'SegmentFile.txt'
vocab_dict_file ='vocab_dict'
abb_list_file='Abb.txt'
output_file='outputfile'
DictionaryFile= dict()
def StartInterface(Query,feeder_number):
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	if(feeder_number in all_feeders):
		if not os.path.exists(str(feeder_number)):
			os.makedirs(str(feeder_number))
			os.chdir(str(feeder_number))
		else:
			os.chdir(str(feeder_number))
		try:
			shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/segment.py',os.getcwd())
			shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/segmentmeta.py',os.getcwd())
			shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/WordFrequencyFeedMetaphone.txt',os.getcwd())
		except:
			0+3
		ExtractDataForFeeder(all_feeders.index(feeder_number))
		ExtractSegmentFile()
		py_compile.compile('segment.py')
		from segment import segment
		with open(SingleFeederAddresses) as f:
			sentence = f.readlines()
		if os.path.isfile('vocab_dict'):
			if feeder_number in DictionaryFile:
				time0 = time.time()
				Answer = AddressCheck(Query,DictionaryFile[feeder_number])
				time1= time.time()
				print ('Time Taken to run this code is '+ str(time1-time0))
			else:
				time0 = time.time()
				DictionaryFile[feeder_number]=(word_cluster(ReturnLongAddressString(sentence)))
				time1= time.time()
				print ('Time Taken to run this code is '+ str(time1-time0))
				Answer = AddressCheck(Query,DictionaryFile[feeder_number])
		else:
			DictionaryFile[feeder_number]=(word_cluster(ReturnLongAddressString(sentence)))
			DictionaryCreation(DictionaryFile[feeder_number])
			Answer = AddressCheck(Query,DictionaryFile[feeder_number])
	else:
		print ('Feeder not in list')
	return Answer

def ExtractDataForFeeder(feeder_index):
	RawAddressList = map(str.lstrip, data[data['50401'] == all_feeders[feeder_index]][data.columns[9]].tolist())
	if os.path.isfile(SingleFeederAddresses):
		print('File exists')
	else:
		file = open(SingleFeederAddresses,'w')
		for x in xrange(len(RawAddressList)):
			file.write(re.sub(' +',' ', RawAddressList[x].translate(None,digits).translate(None,punctuation).strip()+'\n'))
		file.close()
def ExtractSegmentFile():
	if os.path.isfile(SingleFeederAddresses):
		if os.path.isfile(SegmentFile):
			print('Segmentfile Exists')
		else:
			with open(SingleFeederAddresses) as f:
				passage = f.read()
			words = re.findall(r'\w+', passage)
			file = open(SegmentFile,'w')
			word_counts = Counter((words))
			sorted_x = sorted(word_counts.iteritems(), key=operator.itemgetter(0))
			for x in xrange(1,len(sorted_x)):
				if len(sorted_x[x][0].lower())>1 and len(sorted_x[x][0].lower())<9:
					file.write(sorted_x[x][0].lower()+'\t'+str(sorted_x[x][1]*100000)+'\n')
				else:
					2+2
			file.close()
	else:
		print('Data file not available')
		
def ReturnLongAddressString(sentence):
	text1=[]
	from segment import segment
	for x in xrange(len(sentence)):
		sentence[x] = re.sub('[^A-Za-z]+',' ', sentence[x]) 
		temp_segment = segment(sentence[x])# segmented words using Naive Bayes 
		for y in xrange(len(temp_segment)):
			if(len(temp_segment[y])==1):  
				temp_segment[y]='' 
		sentence[x]= " ".join(temp_segment) # Joining words again but with spaces in i
		sentence[x] = re.sub(' +',' ',sentence[x])
		text1.append(sentence[x].strip()) #creating final address strin
	return text1

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
def SimilarityRaw(AddressArray,Suggestion):
	score_raw=[]
	word_area=[]
	score_meta=[]
	if(len(AddressArray)>1):
		answer = doublemetaphone(AddressArray)
		if (len(answer[0])>1):
			AddressMeta=answer[0]
		else:
			AddressMeta=answer[1]
		for y in xrange(len(Suggestion)):
			
			try:
				answer = doublemetaphone(Suggestion[y])
				if (len(answer[0])>1):
					SuggestMeta=answer[0]
				else:
					SuggestMeta=answer[1]
				score_meta.append(jellyfish.jaro_winkler(SuggestMeta,AddressMeta))
				score_raw.append(jellyfish.jaro_winkler(Suggestion[y],AddressArray))
				word_area.append(Suggestion[y])
			except:
				4+4;
	zipped= zip (word_area,score_raw,score_meta)
	finalAnswer =sorted(zipped, key=operator.itemgetter(0))
	return finalAnswer

def RelevantWord(Query,limit):
	score_final=[]
	word_final=[]
	for x in xrange(len(Query)):
		if (Query[x][2]==1.0):
			score_final.append(0.49*Query[x][1]+0.51*Query[x][2])
		else:
			score_final.append(0.68*Query[x][1]+0.32*Query[x][2])
		word_final.append(str(Query[x][0]))
	zipped= zip(word_final,score_final)
	final_Answer =sorted(zipped, key=operator.itemgetter(1),reverse=True)	
	final_Answer = numpy.array(final_Answer)
	return (final_Answer[0:limit])

def SpellCheck(CleanAddStr,wordlist):
	AddressArrayquery = CleanAddStr.lower()
	wordlist = map(lambda s: s.strip(), wordlist)
	AllScore= SimilarityRaw(AddressArrayquery,wordlist)
	NaiveBayesfile = RelevantWord(AllScore,4)
	return NaiveBayesfile

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
