import re
from segment import segment
import enchant	
import os
def CreateAbbList(list_abb):
	abb_list= dict()
	for x in xrange(len(list_abb)):
	#	print (list_abb[x])
		abb_list[list_abb[x].rstrip().split('\t')[0]]=list_abb[x].rstrip().split('\t')[1]
	return abb_list	

abb_list_file='Abb.txt'
if os.path.isfile(abb_list_file):
	with open(abb_list_file) as ab:
		abbrivate=ab.readlines()
else:
	shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/'+abb_list_file,os.getcwd())
	with open(abb_list_file) as ab:
		abbrivate=ab.readlines()
abb_list = CreateAbbList(abbrivate)
with open(SingleFeederAddresses) as f:
	sentence = f.readlines()
for x ub 
Address = '80ahmed'
Address = (''.join( abb_list.get( word, word ) for word in re.split( '(\W+)', Address.lower())))
Address = re.sub(' +','',Address)
print(segment(Address))
