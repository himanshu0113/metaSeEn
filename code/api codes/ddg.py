import urllib
from bs4 import BeautifulSoup
import re
q=raw_input()
query='http://duckduckgo.com/html/?q='+str(q)
site = urllib.urlopen(query)
data = site.read()
parsed = BeautifulSoup(data)

for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
    j=i.a['href'].index('http')
    print urllib.unquote(urllib.unquote(i.a['href'][j:]))

