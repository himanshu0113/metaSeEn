from thread import start_new_thread
#import baidubot
#from baidubot import BaiduBot, scrape_baidu
import urllib
from BeautifulSoup import BeautifulSoup
import re
from bs4 import BeautifulSoup
import urllib, urllib2
from pws import Google
urls = Google.search(query='hello', num=15, start=0, country_code="es")
for i in urls['results']:
	if(i['link'][0]=='h'):
		print i['link']
		print '\n'
