import nltk
import operator
import networkx as nx
with open('outputfile') as f:
    text = f.readlines()


def WordCombination(text):
	G = nx.DiGraph()
	text = map(lambda s: s.strip(), text)
	fDist = nltk.FreqDist(text)
	text = ' '.join(text)
	Most_Common = fDist.most_common(15)
	CommonAddress=[]
	for key in Most_Common:
		CommonAddress.append(key[0])
	str1 = ' '.join(CommonAddress).split(' ')
	Major_words  = list(set(str1))
	Predict=dict()
	Bigram=[]
	for y in xrange(len(Major_words)):
		Predict[Major_words[y]]=0
		indices = [i for i, x in enumerate(str1) if x == str(Major_words[y])]
		temp_dict=dict()
		for k in xrange(len(indices)):
			try:
				if str1[indices[k]+1] in temp_dict:
					2+2
				else:
					temp_dict[str1[indices[k]+1]]=str1.count(str1[indices[k]+1])
					print(Major_words[y]+' '+str1[indices[k]+1])
					print (text.count(Major_words[y]+' '+str1[indices[k]+1]))
	
					Bigram.append(Major_words[y]+' '+str1[indices[k]+1])
					if G.has_edge(Major_words[y],str1[indices[k]+1]):
						weight_edge=  G.get_edge_data(address_list[x][y][0],address_list[x][y+1][0])['weight']
						G.add_edge(address_list[x][y][0],address_list[x][y+1][0],weight=weight_edge+1)
					else:
						G.add_edge(Major_words[y],str1[indices[k]+1],weight=1)
			except:
				2+2
		Predict[Major_words[y]]=temp_dict
	nx.write_dot(G,'dotfile.dot')
	return Predict,G

def MaxiMumInVocab(dictionary,meta): 
	new_temp_list=[]
	if(dictionary.has_key(meta)):
		new_temp_dict=dictionary[meta]
		new_temp_list = new_temp_dict.items()
		new_temp_list = sorted(new_temp_list, key=operator.itemgetter(1),reverse=True)
	else:
		new_temp_list=['nothing','0']
	return new_temp_list[0][0]

[Predict,G] =WordCombination(text)
