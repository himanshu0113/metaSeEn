import csv
a=[]
with open('borda,markov ka copy - Sheet1.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i=0
	ranking = []
	for row in spamreader:
		if(row[0].startswith('http')):
			i = 1
			row[0]=row[0].split(',')
			print row[0]
			ranking.append(int(row[0][1]))
		elif(i==1):
			i = 0
			a.append(ranking)
			ranking = []


#print len(a)


map_score=0
for j in range(len(a)):
	ones_till_now=0
	pr=0
	for i in range(len(a[j])):
		if(a[j][i]==1):
			ones_till_now+=1
			pr+=float(ones_till_now)/float(i+1)	
	pr=float(pr)/a[j].count(1)
	map_score+=pr
	#print pr
map_score=float(map_score)/len(a)
print map_score

