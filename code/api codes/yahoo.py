from bs4 import BeautifulSoup
import urllib, urllib2


# Number of results you need to store from each search engine
numresults = 30 

query = raw_input('Enter Query : ')
yahooResults = []
address = "https://search.yahoo.com/search?p=" + query + "&n=" + str(numresults)
request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko)  Chrome/20.0.1132.57 Safari/536.11'})
urlfile = urllib2.urlopen(request)
page = urlfile.read()
soup = BeautifulSoup(page, "lxml")

urls = []
headers = soup.findAll('h3', {"class": "title"})
for header in headers:
    if not header.a:
        continue
    u = header.a.get('href')
    urls.append(u)

for i in urls:
	print i
