#from IPython.display import HTML
import requests
key = "57b0cd8cdac546c1a4e729586c7e7b00"
assert key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
search_term = "hello"

headers = {"Ocp-Apim-Subscription-Key" : key}
params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML", "responseFilter":"Webpages", "count":50}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()
print 'hello'
for apage in search_results["webPages"]["value"]:
	print apage["url"]


