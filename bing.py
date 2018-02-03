from IPython.display import HTML
import requests

key = "e77311c5c8994d80bcfefe87be962de4"
assert key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
search_term = "IIIT Delhi"

headers = {"Ocp-Apim-Subscription-Key" : key}
params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML", "responseFilter":"Webpages", "count":50}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

for apage in search_results["webPages"]["value"]:
	print apage["url"]


