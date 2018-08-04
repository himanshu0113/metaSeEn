from IPython.display import HTML
import requests
import bs4 as bs
import urllib
import urllib2
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import PorterStemmer
import re
import math
from wordcloud import WordCloud

start = time.time()

key = "e77311c5c8994d80bcfefe87be962de4"
assert key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
search_term = "Britney Spears "

headers = {"Ocp-Apim-Subscription-Key" : key}
params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML", "responseFilter":"Webpages", "count":5}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()



# TOKENINZING QUERRY
Qtoken = word_tokenize(search_term);

QUERRY={}
for key in Qtoken:
	QUERRY[key]={}


DOCID={}  #DOCUMENT ID MAPPING OF ALL URLS
d=0
for apage in search_results["webPages"]["value"]:
	print apage["url"]
	DOCID[d]=apage["url"]




#for apage in search_results["webPages"]["value"]:
#	print apage["snippet"]
#	print ("\n")

#TERM FREQUENCY CALCULATION

i=1
for apage in search_results["webPages"]["value"]:
	sauce = urllib.urlopen(apage["url"]).read()
	soup = bs.BeautifulSoup(sauce, 'lxml')
	document= (soup.get_text())
	DOCTERM=word_tokenize(document)

	

	for term in Qtoken:
		freq=0 
		for wrds in DOCTERM:
			if term == wrds:
				#print "term matched", wrds

				freq+=1
				QUERRY[term][apage["url"]]=math.log10(freq)+1



		




	print("******************************************************************", i)
	i+=1
end = time.time()
print QUERRY






#IDF CALCULATION
IDF={}
for terms in QUERRY:
	print "term is", terms
	
	id = math.log10( float(5) /float(len(QUERRY[terms])))
	IDF[terms]= id
	

print IDF

Rank=[] 

for terms in QUERRY:
	for urls in QUERRY[terms]:
		tf=QUERRY[term][urls]
		idf=IDF[terms]
		tfidf=tf * idf;
		list=[terms, urls, tfidf]
		Rank.append(list)



Rank.sort(key=lambda x: x[2])
print "\n \n"
print Rank
print "time taken: ",end-start


'''{
u'name': u'<b>Complex Systems Lab</b>, <b>IIIT-Delhi</b>', 
u'url': u'http://cosylab.iiitd.edu.in/',
u'dateLastCrawled': u'2018-01-26T13:50:00.0000000Z', 
u'isFamilyFriendly': True, 
u'displayUrl': u'cosylab.<b>iiit</b>d.edu.in', 
u'snippet': u'The research of Ganesh Bagler (<b>IIIT-Delhi</b>) focuses on study of complex systems, primarily of biological origin. We are exploring systems architecture of complex diseases, drug-target networks and brain networks. The broad areas studied in our lab include computational biology, bioinformatics, mathematical modeling, network biology, in silico drug discovery and biomedical text mining. Apart from modeling and analysis of complex systems, we aim to probe for their control mechanisms and ...',
 u'id': u'https://api.cognitive.microsoft.com/api/v7/#WebPages.43'
 }
 '''

