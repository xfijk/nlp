# prepare.py
from POS_2 import *
from EFS import *
# from getStats import *



if __name__ == '__main__':

	# POS=====================================

	T = [('CC',),('CD',),('DT',),('EX',),('FW',),('IN',),
		('JJ',),('JJR',),('JJS',),('LS',),('MD',),('NN',),
		('NNS',),('NNP',),('NNPS',),('PDT',),('POS',),('PRP',),
		('PRP$',),('RB',),('RBR',),('RBS',),('RP',),('TO',),('UH',),
		('VB',),('VBD',),('VBG',),('VBN',),('VBP',),('VBZ',),('WDT',),
		('WP',),('WP$',),('WRB',)]

	m_C_dict = []
	f_C_dict = []
	m_name = 'old.male'
	f_name = 'old.female'
	# m_name = 'm.test'
	# f_name = 'f.test'
	# minsup, minadherence, max_len = 0.3, 0.2, 7
	minsup, minadherence, max_len = 0.1, 0.06, 7

	sys.stderr.write('\n[Reading gzip m]\n')
	tag_seq = readGzipTags(m_name)
	m_total = len(tag_seq)
	sys.stderr.write('\n[Couting stats m]\n')
	m_C_dict = countTags_2(tag_seq, max_len)

	# sys.stderr.write('\n[Writing stats m]\n')
	# writeGzipDict(m_name, m_C_dict, max_len, m_total)

	# sys.stderr.write('\n[Reading stats m]\n')
	# m_C_dict, m_total = readGzipDict(m_name, max_len)


	sys.stderr.write('\n[Mine_POS m]\n')
	T = [x for x in m_C_dict[0] ] 
	SP = mine_POS_pats( m_C_dict, T, minsup, minadherence, max_len, float(m_total))
	writePOS(m_name, SP)


	#==============================================================
	sys.stderr.write('\n[Reading gzip f]\n')
	tag_seq = readGzipTags(f_name)
	f_total = len(tag_seq)
	sys.stderr.write('\n[Couting stats f]\n')
	f_C_dict = countTags_2(tag_seq, max_len)

	# sys.stderr.write('\n[Writing stats f]\n')
	# writeGzipDict(f_name, f_C_dict, max_len, f_total)

	# sys.stderr.write('\n[Reading stats f]\n')
	# f_C_dict, f_total = readGzipDict(f_name, max_len)


	sys.stderr.write('\n[Mine_POS f]\n')
	T = [x for x in f_C_dict[0] ] 
	SP = mine_POS_pats( f_C_dict, T, minsup, minadherence, max_len, float(f_total))
	writePOS(f_name, SP)



	# EFS=====================================
	# max_len = 7
	total = f_total + m_total

	f_c = f_total/total
	m_c = m_total/total

	m_SP = readPOSAll(m_name)
	f_SP = readPOSAll(f_name)
	F = set(m_SP + f_SP)
	# F = ( list(set(m_SP) - set(f_SP)) + list( set(f_SP) - set(m_SP)) )

	# for i in sorted(F):
	# 	print(i)

	rankFeats(F, f_C_dict, m_C_dict, total, f_total, m_total, f_c, m_c )


	# rank_ig = readPOSAllStr('ig')
	# rank_mi = readPOSAllStr('mi')
	# rank_chi = readPOSAllStr('chi')
	# rank_ce = readPOSAllStr('ce')
	# rank_wet = readPOSAllStr('wet')
	# thres = round(len(rank_wet)*0.2) #+ 5
	# # thres = len(list_wet)
	# # thres = 10
	# # thres = 200
	
	# print(len(rank_wet))
	# print(thres)

	# list_feat = sorted(set(rank_ig[:thres] + rank_mi[:thres] + rank_chi[:thres] + rank_ce[:thres] + rank_wet[:thres])) 




	# writePOSAll('mix', list_feat)
	
	# # print(total)

	# list_feat_str = []
	# for feat in sorted(list_feat):
	# 	list_feat_str.append(' '.join(list(feat)))
	# 	# print(feat)

	# # GetStats=====================================
	# m_tags = readGzipTagsStr(m_name)
	# f_tags = readGzipTagsStr(f_name)
	# # t_tags = readGzipTagsStr('test')

	# m_stats = getStats(m_tags, list_feat_str)
	# f_stats = getStats(f_tags, list_feat_str)
	# # t_stats = getStats(t_tags, list_feat_str)

	# writeStats(m_name, m_stats)
	# writeStats(f_name, f_stats)
	# # writeStats('test', t_stats)
