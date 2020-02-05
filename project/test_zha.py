from auxi import *
from collections import defaultdict
import imp
# nltk.download('averaged_perceptron_tagger')

from math import pow # in fairSCP


def fairSCP(seq, C):
	print(seq)
	n = len(seq)
	print(C[n-1][tuple(seq)])

	sum = 0.0

	for i in range(n-1):
		sum += C[i][tuple(seq[:i+1])] * C[n-i-2][tuple(seq[i+1:])]
		print(tuple(seq[:i+1]) , tuple(seq[i+1:]))
		# print(seq[:i+1], seq[i+1:])
		print(i, n-i-2)

	sum /= (n-1)
	print('%.10f '% sum)

	result = pow(C[n-1][tuple(seq)], 2) / sum
	print(result)



def blogs2TagSeq(target):

	# blogs = readGzipBlogs( target + '.blog')
	# writeGzipTags( target + '.tag', blogs)

	
	# writeTags(target + '.tag', blogs)
	tag_seq = readTags(target + '.tag')


	# tag_seq = readGzipTags(target + '.tag')
	return tag_seq




# tag_seq = blogs2TagSeq('male')
# tag_seq = blogs2TagSeq('female')
tag_seq = blogs2TagSeq('all')

# for i in tag_seq: print(i)

def countTags(max_len):
	total = [0]*max_len
	C = []
	stat = []

	for i in range(max_len):
		C.append(defaultdict(float))

	for n in range(1,max_len+1):
		for tags in tag_seq:
			for i in range(len(tags)+1-n):
				elem = ()
				for l in range(n):
					elem += (tags[i+l],)

				C[n-1][elem] += 1
				total[n-1] += 1
		
	for i in range(max_len):
		for k in C[i]:
			C[i][k] /= float(total[i])

	return C, total



max_len = 4
C, total = countTags(max_len)
for i in range(max_len):
	for k in sorted(C[i], key=C[i].get, reverse=True ):
		print(k, C[i][k] )

print(total)


fairSCP(['NN', '.', 'PRP'], C)



