from collections import Counter
from thread import start_new_thread
import timeit
#import baidubot
#from baidubot import BaiduBot, scrape_baidu
import urllib
import re
from pws import Google
from bs4 import BeautifulSoup
import urllib, urllib2
import json 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import bs4 as bs
import math
import time

with open('cache.json', 'r') as jfile:
   	cache = json.load(jfile)


google_link=[]
global g
g=0
bing_link=[]
global bi
bi=0
baidu_link=[]
global ba
ba=0
yahoo_link=[]
global y
y=0
ddg_link=[]
global d
d=0
all_links=[]
final_link_results=[]
global cl
cl = 0

def google(query):
	try:
		urls = Google.search(query, num=10, start=0, country_code="es")
		for i in urls['results']:
			if(i['link'][0]=='h'):
				google_link.append(i['link'])
				all_links.append(i['link'])
	except:
		pass
	global g
	g=1	

def bing(query):
	import requests
	key = "57b0cd8cdac546c1a4e729586c7e7b00"
	assert key
	search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
	headers = {"Ocp-Apim-Subscription-Key" : key}
	params  = {"q": query, "textDecorations":True, "textFormat":"HTML", "responseFilter":"Webpages", "count":10}
	response = requests.get(search_url, headers=headers, params=params)
	response.raise_for_status()
	search_results = response.json()
	for apage in search_results["webPages"]["value"]:
		bing_link.append(apage["url"])
		all_links.append(apage["url"])
	global bi
	bi=1


def baidu(query):
	query= 'http://www.baidu.com/s?wd='+str(query)+'&pn=10'
	site = urllib.urlopen(query)
	data = site.read()
	soup = BeautifulSoup(data)
	link_start='http://www.baidu.com/link?url='
	cnt=0
	for i in soup.findAll('div', {'class': re.compile('f13')}):
		j=i.a['href']
		if(j.startswith(link_start)):
			baidu_link.append(j)
			all_links.append(j)
			cnt+=1
			if(cnt>=9):
				break
	global ba
	ba=1
def ddg(search):
	try:
		query='http://duckduckgo.com/html/?q='+str(search)
		site = urllib.urlopen(query)
		data = site.read()
		parsed = BeautifulSoup(data)
		cnt=0
		for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
			j=i.a['href'].index('http')
			ddg_link.append(urllib.unquote(urllib.unquote(i.a['href'][j:])))
			all_links.append(urllib.unquote(urllib.unquote(i.a['href'][j:])))
			cnt+=1
			if(cnt>=10):
				break
	except:
		pass
	global d
	d=1
	

def yahoo(query):
	try:
		numresults = 10 
		yahooResults = []
		address = "https://search.yahoo.com/search?p=" + query + "&n=" + str(numresults)
		request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like 	Gecko)  Chrome/20.0.1132.57 Safari/536.11'})
		urlfile = urllib2.urlopen(request)
		page = urlfile.read()
		soup = BeautifulSoup(page, "lxml")
		urls = []
		headers = soup.findAll('h3', {"class": "title"})
		cnt=0
		for header in headers:
			if not header.a:
				continue
			u = header.a.get('href')
			urls.append(u)
			cnt+=1
			if(cnt>=10):
				break
		for i in urls:
			yahoo_link.append(i)
			all_links.append(i)
	except:
		pass
	global y
	y=1

def tf_idf(query , search_results):
	start = time.time()
	# TOKENINZING QUERRY
	Qtoken = word_tokenize(query);
	QUERRY={}
	RANK_INDEX={}
	for key in Qtoken:
		QUERRY[key]={}
	DOCID={}  #DOCUMENT ID MAPPING OF ALL URLS
	d=0
	for apage in search_results:
		RANK_INDEX[apage]={}
	#TERM FREQUENCY CALCULATION
	i=1
	for apage in search_results:
		#print apage+"ojasvi"
		try:
			sauce = urllib.urlopen(apage).read()
			soup = bs.BeautifulSoup(sauce, 'lxml')
			data= soup
			document=''
			for text in data.findAll('p'):
				document+=text.getText()
			DOCTERM=word_tokenize(document)
			for term in Qtoken:
				freq=0 
				if term in DOCTERM:
					freq=DOCTERM.count(term)
					QUERRY[term][apage]=math.log10(freq)+1
					RANK_INDEX[apage][term]=math.log10(freq)+1
				else:
					QUERRY[term][apage]=1
					RANK_INDEX[apage][term]=1
		except:
			#print 'Exception'
			for term in Qtoken:
				QUERRY[term][apage]=1
				RANK_INDEX[apage][term]=1
		print("******************************************************************",i)
		i+=1
	end = time.time()
	#IDF CALCULATION
	#print QUERRY
	IDF={}
	for terms in QUERRY:
		ids = math.log10( float(len(search_results)) /float(len(QUERRY[terms])))
		if(ids==0):
			ids=1
		IDF[terms]= ids
	#print RANK_INDEX
	Rank=[]
	for links in RANK_INDEX:
		link_scr=0
		if(len(RANK_INDEX[links])>0):
			for terms in RANK_INDEX[links]:
				#print terms+"  ,  "+links
				tf=QUERRY[terms][links]
				idf=IDF[terms]
				link_scr+=tf*idf
		lists=[links,link_scr]
		Rank.append(lists)
	'''
	for website in Rank:
		wot_sc = web_of_trust(website[0])
		ind = Rank.index(website)
		website[1] = website[1] + wot_sc
		Rank[ind] = website
	'''
	Rank.sort(key=lambda x: x[1])
	#print Rank
	rlen = len(Rank)
	global final_link_results
	while(rlen>-1):
		print Rank[rlen-1]
		final_link_results.append(Rank[rlen-1])
		rlen = rlen -1	
	#print "time taken: ",end-start
	global cl
	cl = 1


def web_of_trust(website):
	url = None
	if '.com' in website:
		ind = website.index('.com')
		url = 'http://api.mywot.com/0.4/public_link_json2?hosts='+website[:ind+4]+'/&callback=process&key=f2611810521b7bb56215f0b2cacbd905257d7aa8'
	elif '.in' in website:
		ind = website.index('.in')
		url = 'http://api.mywot.com/0.4/public_link_json2?hosts='+website[:ind+3]+'/&callback=process&key=f2611810521b7bb56215f0b2cacbd905257d7aa8'
	elif '.gov' in website:
		ind = website.index('.gov')
		url = 'http://api.mywot.com/0.4/public_link_json2?hosts='+website[:ind+4]+'/&callback=process&key=f2611810521b7bb56215f0b2cacbd905257d7aa8'
	else:
		url = 'http://api.mywot.com/0.4/public_link_json2?hosts='+website+'/&callback=process&key=f2611810521b7bb56215f0b2cacbd905257d7aa8'
	wot_score = 0
	print "website is " + str(website)
	response = urllib2.urlopen(url).read()
	#print " ** WEB of TRUST Results ** "
	#print response[8:-1]
	resp_dict = json.loads(response[8:-1])
	#print resp_dict
	for key in resp_dict:
		if(resp_dict[key].get('0')):
			score = resp_dict[key]['0']
			wot_score = float(float(score[0])*float(score[1])/float(1000))
			#print resp_dict[key]['0']
	#print " Website score is : " + str(wot_score)
	return wot_score


def analysis(clen,all_len):
	labels = 'Common Links', 'Uncommon Links'
	sizes = []
	sizes.append(clen)
	sizes.append(all_len-clen)
	colors = ['gold', 'lightcoral']
	explode = (0.1, 0,) 
	plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	plt.show()

def main():
	query = raw_input('Enter Query : ')
	for key in cache:
		if(key==query):
			print "\n###  Query fetched from cache ###### \n"
			post = cache[key]
			for num in range(0, len(post)):
				print post[num]
			exit()
	print "\nQuery not present in cache ......... \n"
	st=timeit.default_timer()
	start_new_thread(bing,(query,))
	start_new_thread(baidu,(query,))
	start_new_thread(google,(query,))
	start_new_thread(ddg,(query,))
	start_new_thread(yahoo,(query,))
	cnt=0
	common_link=[]
	while((g!=1 or d!=1 or y!=1 or bi!=1 or ba!=1) and ((timeit.default_timer()-st)<20) ):
		print "g= "+str(g)+", d= "+str(d)+", bi= "+str(bi)+", y= "+str(y)+", ba= "+str(ba)
		print timeit.default_timer()-st
		pass
	cnt = Counter(all_links)
	common_links=[	'http://www.crackthemba.com/directions/',
			'http://www.indiaeducation.net/iiit/delhi/contacts.aspx',
			'https://www.quora.com/How-do-I-reach-IIIT-Delhi-from-Delhi-Airport']
#	print len(set(all_links))
	print "Google "
	print google_link
	print "DDG "
	print ddg_link
	print "Yahoo "
	print yahoo_link
	print "Bing"
	print bing_link
#	set_all_links=set(set_all_links)
#	uncommon_links=all_links-common_links
	uncommon_links=list(set(all_links)-set(common_links))
	
	print "\n\n ** Common links ** \n"
	for element in common_links:
		print element
	print "len cmn links=" +str(len(common_links))
	print "\n\n ** Uncommon links ** \n "
	for element in uncommon_links:
		print element
	print "len uncmn links=" +str(len(uncommon_links))
	borda_link_score=[]
	borda_links=[]
	for link in common_links:
		borda_links.append(link)
		bscore=0
		if link in google_link:
			bscore+=1
		if link in yahoo_link:
			bscore+=1
		if link in ddg_link:
			bscore+=1
		if link in bing_link:
			bscore+=1
		if link in baidu_link:
			bscore+=1
		borda_link_score.append(bscore)
	borda_link_score, borda_links = zip(*sorted(zip(borda_link_score, borda_links)))	
	#analysis(len(common_links),len(list(set(all_links))))
	if(len(borda_links)<10):
		print "\n\n ** checking of tf-idf for uncommon links ** \n\n"
		start_new_thread(tf_idf,(query,uncommon_links,))
		while(cl!=1):
			pass
		#final_link_results = borda_links
		global final_link_results
		final_link_results=final_link_results[0:(10-len(borda_links))]
	#reversing links to bring high score links to top
	borda_links=borda_links[::-1]
	borda_link_score=borda_link_score[::-1]	
	borda_links=list(borda_links)
	global final_link_results	
	for i in range(len(final_link_results)):
		final_link_results[i]=final_link_results[i][0]
	if(len(borda_links)<10):
		for link in final_link_results:
			if link not in borda_links:
				borda_links.append(link)
	print "\n\n ** Top 10 Results ** \n\n"
	for i in range(len(borda_links)):
		print borda_links[i]
	if(len(cache)<=50):
		cache[query] = list(final_link_results)
	else:	
		cache.pop(0)
		cache[query] = list(final_link_results)	
	'''
	with open('cache.json', 'w') as jfile:
    		json.dump(cache, jfile)	
	'''
main()

