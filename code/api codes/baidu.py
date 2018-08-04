import urllib
from bs4 import BeautifulSoup
import re
print'input'
q=raw_input()
query= 'http://www.baidu.com/s?wd='+str(q)+'&pn=10'
print query
site = urllib.urlopen(query)
data = site.read()
soup = BeautifulSoup(data)
#print soup
link_start='http://www.baidu.com/link?url='
cnt=0
for i in soup.findAll('div', {'class': re.compile('f13')}):
	j=i.a['href']
	if(j.startswith(link_start)):
		print j
		cnt+=1
		if(cnt==9):
			break

