import math
import csv

with open('borda ka copy - Sheet1.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i=0
	ranking_list = []
	ranking = []
	for row in spamreader:
		if(row[0].startswith('http')):
			print row[0]
			i = 1
			row[0]=row[0].split(',')
			ranking.append(int(row[0][3]))
		elif(i==1):
			i = 0
			ranking_list.append(ranking)
			ranking = []

print len(ranking_list)

num = 1
for el in ranking_list:
	print el
	print num
	num+=1

final_ndgc = []

for aquery in ranking_list:
	print "Original rank "
	print aquery
	print " Ideal Rank "
	ideal_rank = sorted(aquery)
	print ideal_rank
	i = 1
	dcg = 0.0
	ndgc = 0.0
	for num in range(0,len(aquery)):
	#rel = float(aquery[num])/float(10)
		rel = float(10)- float(aquery[num])
		print "Rel is " + str(rel)
		numer = 2**rel-1
		print "Numer" + str(num)
		n = i+1
		denom = math.log(n , 2)
		dcg = dcg + float(numer)/float(denom)
	#irel = float(ideal_rank[num])/float(10)
		irel = float(10)- float(ideal_rank[num])
		idealn= 2**irel-1
		ndgc=ndgc+ float(idealn)/float(denom)
		i = i+1
	ndgc_score = float(dcg)/float(ndgc)
	final_ndgc.append(ndgc_score)
	

print "NDGC score accross all queries :"
print final_ndgc
print sum(final_ndgc)/len(final_ndgc)

