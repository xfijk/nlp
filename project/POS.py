from auxi import *

from copy import deepcopy

def fairSCP(seq, C_dict, total):
	n = len(seq)

	sum = 0.0

	for i in range(n-1):
		sum += C_dict[i][tuple(seq[:i+1])]/total * C_dict[n-i-2][tuple(seq[i+1:])]/total

	sum /= (n-1)

	result = pow(C_dict[n-1][tuple(seq)]/total, 2) / sum
	return result


def candidate_gen(C, F, k, T):
	for c in F[k-1]:
		for t in T:
			C[k].append( (c+t) ) 



def mine_POS_pats( C_dict, T, minsup, minadherence, max_len, total):
	
	C = []
	F = []
	SP = []
	for i in range(max_len):
		C.append([])
		F.append([])
		SP.append([])

	for tag in T:
		if C_dict[0][tag]/total >= minsup:
			F[0].append(tag)

	SP[0] = deepcopy(F[0])

	for k in tqdm(range(1, max_len)):
		candidate_gen(C, F, k, T)

		for tag_seq in C[k]:
			if C_dict[k][tag_seq]/total >= minsup:
				F[k].append(tag_seq)

		for tag_seq in F[k]:
			if fairSCP(tag_seq, C_dict, total) >= minadherence:
				SP[k].append(tag_seq)

	return SP
	# return SP[1:]



if __name__ == '__main__':


	T = [('CC',),('CD',),('DT',),('EX',),('FW',),('IN',),
	('JJ',),('JJR',),('JJS',),('LS',),('MD',),('NN',),
	('NNS',),('NNP',),('NNPS',),('PDT',),('POS',),('PRP',),
	('PRP$',),('RB',),('RBR',),('RBS',),('RP',),('TO',),('UH',),
	('VB',),('VBD',),('VBG',),('VBN',),('VBP',),('VBZ',),('WDT',),
	('WP',),('WP$',),('WRB',)]

	m_C_dict = []
	f_C_dict = []
	m_name = 'm.dev'
	f_name = 'f.dev'
	minsup, minadherence, max_len = 0.3, 0.2, 7



	# sys.stderr.write('\n[Reading gzip m]\n')
	# tag_seq = readGzipTags(m_name)
	# total = len(tag_seq)
	# sys.stderr.write('\n[Couting stats m]\n')
	# m_C_dict = countTags_2(tag_seq, max_len)

	# sys.stderr.write('\n[Writing stats m]\n')
	# writeGzipDict(m_name, m_C_dict, max_len, total)

	sys.stderr.write('\n[Reading stats m]\n')
	m_C_dict, total = readGzipDict(m_name, max_len)

	# normalizeCount(m_C_dict, total)

	# # for i in range(max_len):
	# # 	for k in sorted(m_C_dict[i], key=m_C_dict[i].get, reverse=True ):
	# # 		print(k, m_C_dict[i][k] )

	sys.stderr.write('\n[Mine_POS m]\n')
	# T = [x for x in m_C_dict[0] ] 
	pp.pprint(T)
	SP = mine_POS_pats( m_C_dict, T, minsup, minadherence, max_len, float(total))
	writePOS(m_name, SP)


	#==============================================================
	# sys.stderr.write('\n[Reading gzip f]\n')
	# tag_seq = readGzipTags(f_name)
	# total = len(tag_seq)
	# sys.stderr.write('\n[Couting stats f]\n')
	# f_C_dict = countTags_2(tag_seq, max_len)

	# sys.stderr.write('\n[Writing stats f]\n')
	# writeGzipDict(f_name, f_C_dict, max_len, total)

	sys.stderr.write('\n[Reading stats f]\n')
	f_C_dict, total = readGzipDict(f_name, max_len)

	# normalizeCount(f_C_dict, total)

	# # for i in range(max_len):
	# # 	for k in sorted(f_C_dict[i], key=f_C_dict[i].get, reverse=True ):
	# # 		print(k, f_C_dict[i][k] )

	sys.stderr.write('\n[Mine_POS f]\n')
	# T = [x for x in f_C_dict[0] ] 
	pp.pprint(T)
	SP = mine_POS_pats( f_C_dict, T, minsup, minadherence, max_len, float(total))
	writePOS(f_name, SP)





