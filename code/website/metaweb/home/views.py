from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from collections import Counter
from thread import start_new_thread
import timeit
#import baidubot
#from baidubot import BaiduBot, scrape_baidu
import urllib
import re
from . import Google
from bs4 import BeautifulSoup
import urllib, urllib2
import json 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import bs4 as bs
import math
import time
from operator import itemgetter 
import numpy as np
import math
#from IPython.display import HTML
import requests


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
	key = "f7e0213e001340efb1ef905632e8a456"
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

# =============================================================================
# 
# =============================================================================

def buildTransition(inputLists, space):
    nList = len(inputLists)
    
    topK = space[:]
    
    for i in range(nList):
        n = len(inputLists[i])
        topKList = [n]*len(space[i])
        indices = []
        for j in range(len(inputLists[i])):
            indices.append(space[i].index(inputLists[i][j]))
        
        j = 0
        for idx in indices:
            topKList[idx] = j
            j+=1
        
        topK[i] = topKList
        
    L = list(set([x for l in inputLists for x in l]))
    N = len(L)
    
    MC1 = np.zeros((N,N))
    MC2 = np.zeros((N,N))
    MC3 = np.zeros((N,N))
    
    lookup = []
    for l1 in L:
        for l2 in L:
            if l1!=l2:
                temp = [l1, l2]
                lookup.append(temp)
    
    for i in range(len(lookup)):
        a = lookup[i][0]
        b = lookup[i][1]
        found = 0
        nn = 0
        for j in range(nList):
            found += (a in space[j])*(b in space[j])
            nn += (topK[j][space[j].index(a)]>
                        topK[j][space[j].index(b)])
            
        index1 = L.index(a)
        index2 = L.index(b)
        
        MC1[index1, index2] = math.ceil(float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        MC2[index1, index2] = math.floor(float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        MC3[index1, index2] = (float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        
    MC1=MC1/float(N)
    MC2=MC2/float(N)
    MC3=MC3/float(N)
     

    for i in range(N):
        MC1[i,i]=1-sum(MC1[i])
        MC2[i,i]=1-sum(MC2[i])
        MC3[i,i]=1-sum(MC3[i])
  
    return L, MC1, MC2, MC3

def MC_ranks(elements, trans, a = 0.15, delta = 0.011):
#        print "elements are: ", elements
#        print " trans matrix is", trans
        n=trans.shape[0] # number of rows
        trans= trans * float((1-a)) # multiply and add all elements
        trans= trans + float(a)/float(n)
        A= np.zeros((n,n))
        for x in range(n):
                A[x,x]=1

        difference= 1
        count=0
        while difference>delta:
#                print " converging"
                A1= np.matmul(A,trans)
#                print " the matrix is: \n ", A1
                temp= A1-A
#                print "TEM MATRX IS :"
#                print temp
                difference= float(temp.max())
                #if difference== 0.0:
                 #       break
#                print "difference is: ",difference
                A= A1
                count+=1


        # Aaauming A1 in a 1 x n matrix
        #Assuming Elements= [a,b,c,d]
        
        A1= A1[0,:] #get first row of the matrix
        temp=A1.tolist() # temp should have this structure [n1, n2, n3]
        ranked_ele=[]
        for i in range(n):
                max_ele=max(temp)
                index= temp.index(max_ele)
                element=elements[index]
                ranked_ele.append(element)
                temp[index]=-1

        A1= -np.sort(-A1)
        results=[]
        results.append(count)
        results.append(A1)
        results.append(ranked_ele)
#        print ranked_ele

        return results

def MC(inputLists, k=0, a=0.15, delta=10^-15):    
    space = list(set([x for l in inputLists for x in l]))
    space.sort();
    space = [space]*len(inputLists)
    
    
    L, MC1, MC2, MC3 = buildTransition(inputLists, space)
    
    N =len(L)
    if k ==0:
        k = N
    
    MC1Ranks = MC_ranks(L, MC1)
    MC2Ranks = MC_ranks(L, MC2)
    MC3Ranks = MC_ranks(L, MC3)

#    print MC1
#    print MC2
#    print MC3    

    print MC1Ranks[2], MC1Ranks[1]
    print MC2Ranks[2], MC2Ranks[1]
    print MC3Ranks[2], MC3Ranks[1]
    
    print "/n/n ************* RESULT *********************"
    top=0
    final=[]
    for ele in MC3Ranks[2]:
        print ele
        final.append(ele)
        top+=1
        if(top==10):
            break
    return final

# Create your views here.
def index(request):
	if request.method == 'POST':
		query = request.POST['Search']
		print query
		st=timeit.default_timer()
		start_new_thread(bing,(query,))
		start_new_thread(baidu,(query,))
		start_new_thread(google,(query,))
		start_new_thread(ddg,(query,))
		start_new_thread(yahoo,(query,))
		
		
		while((g!=1 or d!=1 or y!=1 or bi!=1 or ba!=1) and ((timeit.default_timer()-st)<20) ):
			pass
		
		print "Google "
		print google_link
		print "DDG "
		print ddg_link
		print "Yahoo "
		print yahoo_link
		print "Bing"
		print bing_link
		
		lists = []
		lists.append(google_link)
		lists.append(ddg_link)
		lists.append(yahoo_link)
		lists.append(bing_link)
		print query
		srch=MC(lists)
		
		return render_to_response('home/srch_res.html', {'search': srch}, context_instance=RequestContext(request))
	else:
		return render(request,'home/home.html')





'''
    if request.method == 'POST':
	        key = "f7e0213e001340efb1ef905632e8a456"
		assert key

		search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
		search_term = "IIIT Delhi"
		
		headers = {"Ocp-Apim-Subscription-Key" : key}
		params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML", "responseFilter":"Webpages", "count":50}
		response = requests.get(search_url, headers=headers, params=params)
		response.raise_for_status()
		search_results = response.json()
		srch=[]
		for apage in search_results["webPages"]["value"]:
			srch.append(apage["url"])

		return render_to_response('home/srch_res.html', {'search': srch}, context_instance=RequestContext(request))
	else:
		return render(request,'home/home.html')
'''
