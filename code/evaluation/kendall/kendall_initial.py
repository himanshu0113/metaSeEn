import math
import csv
import re

with open('IR annotation initial model - DELHI METRO.csv', 'rb') as csvfile:
	print "file openned"
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i=0
	print "reading"
	ranking_list = []
	ranking = []

	for row in spamreader:
		row[0]=row[0].split(',')
		print (row[0][0])

		searchObj = re.match( r'\"\d+', row[0][0])
		print searchObj

		if searchObj:									#re.search(r"\d+", row[0]):
			i = 1
			print row[0]
			#
			print row[0]

			ranking.append(int(row[0][3]))
		else:
			i = 0
			ranking_list.append(ranking)
			ranking = []


print ranking_list

evaluate_list=[]

for row in ranking_list:
	if row==[]:
		print "empty"
	else:
		evaluate_list.append(row)

print evaluate_list
print len(evaluate_list)

score={}
i=0
for element in evaluate_list:
	score[i]=0

	for ele in element:
		if ele==1:
			score[i]+=1

	score[i]=float(score[i])/float(45)
	i+=1

Total=0
for s in score:
	print s, "->", score[s]
	Total=Total+score[s]

print "Average kendall distance for this model",float(Total)/float(len(evaluate_list))





